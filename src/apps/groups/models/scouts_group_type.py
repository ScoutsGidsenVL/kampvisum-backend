from django.db import models

from apps.groups.managers import ScoutsGroupTypeManager

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, UniqueBooleanField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupType(AbstractBaseModel):
    """
    Specifies the type of scouts group (e.g. AKABE, zeescouts, ...).
    """

    objects = ScoutsGroupTypeManager()

    group_type = RequiredCharField("type", max_length=64)
    parent = models.ForeignKey(
        "ScoutsGroupType", null=True, on_delete=models.CASCADE, verbose_name="bovenliggend type"
    )
    is_default = UniqueBooleanField("standaard", default=False)

    class Meta:
        ordering = ["group_type"]
        constraints = [models.UniqueConstraint(fields=["group_type"], name="unique_group_type")]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED ScoutsGroupType")
        return (self.group_type,)

    def __str__(self):
        return self.group_type

    def to_simple_str(self):
        return "{}".format(self.group_type)
