from django.db import models

from apps.camps.managers import CampYearManager

from scouts_auth.inuits.models import AuditedBaseModel

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampYear(AuditedBaseModel):
    """
    Represents a scouts year.

    A camp year starts on the 1st of September and ends on the 31st of August
    of the next calendar year, but will be displayed as the next calendar year
    (the year that the camp will actually take place).
    e.g. the displayed year for a CampYear that starts on 01/09/2021 is 2022
    """

    objects = CampYearManager()

    year = models.IntegerField("jaar")
    start_date = models.DateField("startdatum")
    end_date = models.DateField("einddatum")

    class Meta:
        ordering = ["year"]
        indexes = [models.Index(fields=["year"], name="year_idx")]
        constraints = [models.UniqueConstraint(fields=["year"], name="unique_year")]

    def natural_key(self):
        # logger.trace("NATURAL KEY CALLED CampYear")
        return (self.year,)

    def __str__(self):
        return f"Kampjaar {self.year}"

    def to_simple_str(self):
        return "{}".format(self.year)
