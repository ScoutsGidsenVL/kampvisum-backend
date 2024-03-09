import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler

from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.mail import EmailServiceException

logger: InuitsLogger = logging.getLogger(__name__)


def drf_exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception"""
    logger.error(f"{exc.__class__.__name__}: {exc}")
    if isinstance(exc, ScoutsAuthException) and exc.has_cause():
        logger.error(f"Caused by: {exc.cause.__class__.__name__}: {exc.cause}")
    elif isinstance(exc, DRFAuthenticationFailed):
        logger.debug("AUTHENTICATION FAILED")
    elif isinstance(exc, DjangoValidationError):
        try:
            detail = exc.message_dict
        except Exception:
            detail = exc.messages
        exc = DRFValidationError(detail=detail)
    elif isinstance(exc, EmailServiceException):
        exc = EmailServiceException(exc)

    response = exception_handler(exc, context)

    if response is not None:
        if hasattr(response, "data") and isinstance(response.data, dict):
            response.data["status_code"] = 422
        else:
            response.status = 422

    return response
