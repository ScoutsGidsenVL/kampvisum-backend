from django.db import models

from apps.camps.models import CampYear
from apps.camps.managers import CampManager
from apps.groups.models import ScoutsSection

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalDateField

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Camp(AuditedBaseModel):
    """
    A model for a scouts camp.
    """

    objects = CampManager()

    # @TODO model period, exceptions, test-driven
    year = models.ForeignKey(CampYear, on_delete=models.CASCADE)
    name = models.TextField()
    start_date = OptionalDateField()
    end_date = OptionalDateField()
    sections = models.ManyToManyField(ScoutsSection)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return "OBJECT Camp: year({}), name({}), start_date({}), end_date({}), sections({})".format(
            str(self.year),
            self.name,
            self.start_date,
            self.end_date,
            str(self.sections),
        )

    def to_simple_str(self):
        return "Camp ({}), {} {}".format(self.id, self.year.year, self.name)
