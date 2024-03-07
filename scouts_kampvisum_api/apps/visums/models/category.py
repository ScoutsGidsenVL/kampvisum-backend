# LOGGING
import logging

from django.db import models

from apps.camps.models import CampType, CampYear
from apps.visums.managers import CategoryManager
from apps.visums.models import CategoryPriority
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.models import ArchiveableAbstractBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.mixins import Describable, Explainable, Indexable, Translatable

logger: InuitsLogger = logging.getLogger(__name__)


class Category(Describable, Explainable, Indexable, Translatable, ArchiveableAbstractBaseModel):
    objects = CategoryManager()

    name = RequiredCharField(max_length=128)
    camp_year = models.ForeignKey(CampYear, on_delete=models.CASCADE, related_name="categories")
    camp_types = models.ManyToManyField(CampType)
    # Indicates the hierarchical source and thereby specifies precedence.
    priority = models.ForeignKey(
        CategoryPriority,
        on_delete=models.CASCADE,
        default=None,
    )

    class Meta:
        ordering = ["index"]
        constraints = [
            models.UniqueConstraint(fields=["name", "camp_year"], name="unique_category_name_and_camp_year")
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED Category")
        return (self.name, self.camp_year)

    def __str__(self):
        return "OBJECT Category: id ({}), name({}), camp_year ({}), priority ({}) label({}), index({}), description({}), explanation ({}), camp_types ({})".format(
            self.id,
            self.name,
            self.camp_year,
            self.priority,
            self.label,
            self.index,
            self.description,
            self.explanation,
            ", ".join(camp_type.camp_type for camp_type in self.camp_types.all()) if self.camp_types else "[]",
        )

    def to_simple_str(self):
        return "{} ({})".format(self.name, self.id)
