from django.db import models

from apps.camps.models import CampYear, CampType

from apps.deadlines.managers import DeadlineManager

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import RequiredCharField
from scouts_auth.inuits.models.mixins import (
    Describable,
    Explainable,
    Indexable,
    Translatable,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Deadline(Describable, Explainable, Indexable, Translatable, AuditedBaseModel):
    objects = DeadlineManager()

    name = RequiredCharField("naam")
    is_important = models.BooleanField(default=False)
    is_camp_registration = models.BooleanField(default=False)
    camp_year = models.ForeignKey(
        CampYear, on_delete=models.CASCADE, related_name="deadline_set", verbose_name="kampjaar"
    )
    camp_types = models.ManyToManyField(CampType, related_name="deadlines")

    class Meta:
        ordering = [
            "index",
            "due_date__date_year",
            "due_date__date_month",
            "due_date__date_day",
            "is_important",
            "name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "camp_year"],
                name="unique_name__camp_year",
            )
        ]

    def natural_key(self):
        logger.trace("NATURAL KEY CALLED Deadline")
        return (self.name, self.camp_year)

    def __str__(self) -> str:
        due_date = getattr(self, "due_date", None)
        if due_date and due_date.date_day and due_date.date_month and due_date.date_year:
            return "Deadline {} {}: {:02d}/{:02d}/{}".format(
                self.label, self.camp_year.year, due_date.date_day, due_date.date_month, due_date.date_year
            )
        return "Deadline {} {}".format(self.label, self.camp_year.year)
