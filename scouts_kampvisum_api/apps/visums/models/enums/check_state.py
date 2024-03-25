"""apps.visums.models.enums.check_state."""
import logging

from django.db import models
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CheckState(models.TextChoices):
    EMPTY = "EMPTY", "Empty"
    UNCHECKED = "UNCHECKED", "Unchecked"
    CHECKED = "CHECKED", "Checked"
    NOT_APPLICABLE = "NOT_APPLICABLE", "Not applicable"

    @staticmethod
    def is_checked_or_irrelevant(state) -> bool:
        if state == CheckState.CHECKED or state == CheckState.NOT_APPLICABLE:
            return True

        return False

    @staticmethod
    def is_unchecked(state) -> bool:
        if state == CheckState.UNCHECKED:
            return True
        return False
