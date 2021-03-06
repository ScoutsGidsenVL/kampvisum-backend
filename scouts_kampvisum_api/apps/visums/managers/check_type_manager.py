from django.db import models


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckTypeManager(models.Manager):
    """
    Loads CheckType instances by their name, not their id.

    This is useful for defining fixtures.
    """

    def get_by_natural_key(self, check_type):
        logger.trace(
            "GET BY NATURAL KEY %s: (check_type: %s (%s))",
            "CheckType",
            check_type,
            type(check_type),
        )
        return self.get(check_type=check_type)
