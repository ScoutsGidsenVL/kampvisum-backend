from django.db import models

from apps.camps.models import CampType

from apps.visums.managers import CheckManager
from apps.visums.models import SubCategory, CheckType

from scouts_auth.inuits.models import ArchiveableAbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField, OptionalCharField
from scouts_auth.inuits.models.mixins import (
    Changeable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Check(
    Changeable,
    Explainable,
    Indexable,
    Linkable,
    Translatable,
    ArchiveableAbstractBaseModel,
):
    objects = CheckManager()

    name = RequiredCharField("naam", max_length=64)
    is_multiple = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_required_for_validation = models.BooleanField(default=True)
    requires_permission = OptionalCharField()
    linked_to = OptionalCharField()
    change_handlers = OptionalCharField()
    validators = OptionalCharField()
    sub_category = models.ForeignKey(
        SubCategory, related_name="checks", on_delete=models.CASCADE, verbose_name="subcategorie"
    )
    check_type = models.ForeignKey(CheckType, on_delete=models.CASCADE, verbose_name="type")
    camp_types = models.ManyToManyField(CampType)

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "sub_category")

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED Check")
        return (self.name, self.sub_category)

    def __str__(self):
        return self.label if self.has_label() else self.name

    def to_simple_str(self) -> str:
        return "{} ({})".format(self.name, self.id)
