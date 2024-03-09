"""apps.deadlines.models.linked_deadline."""

import logging

from django.db import models
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.models import AuditedBaseModel

from apps.deadlines.managers import LinkedDeadlineManager
from apps.deadlines.models import Deadline
from apps.visums.models import CampVisum

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadline(AuditedBaseModel):
    objects = LinkedDeadlineManager()

    parent = models.ForeignKey(Deadline, on_delete=models.CASCADE, related_name="deadline")
    visum = models.ForeignKey(CampVisum, on_delete=models.CASCADE, related_name="deadlines")

    class Meta:
        ordering = ["parent"]
        unique_together = ("parent", "visum")

    def __str__(self):
        return "visum ({}), parent({})".format(self.visum.id, self.parent)
