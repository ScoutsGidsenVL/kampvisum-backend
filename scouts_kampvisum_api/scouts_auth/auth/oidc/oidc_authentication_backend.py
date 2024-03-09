import logging

from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    pass
