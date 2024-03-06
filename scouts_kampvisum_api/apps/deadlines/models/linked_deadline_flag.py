"""apps.deadlines.models.linked_deadline_flag."""
# LOGGING
import logging

from django.db import models

from apps.deadlines.managers import LinkedDeadlineFlagManager
from apps.deadlines.models import DeadlineFlag
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.models import AuditedBaseModel

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineFlag(AuditedBaseModel):

    objects = LinkedDeadlineFlagManager()

    parent = models.ForeignKey(DeadlineFlag, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)
    
    def is_checked(self) -> bool:
        return self.flag
