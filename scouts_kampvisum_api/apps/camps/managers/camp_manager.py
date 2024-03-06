"""apps.camps.managers.camp_manager."""
# LOGGING
import logging
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsGroup
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CampManager(models.Manager):
    """
    Loads CampYear instances by their integer year, not their id/uuid.

    This is useful for defining fixtures.
    """

    def get_queryset(self):
        return CampQuerySet(self.model, using=self._db)
