"""apps.deadlines.models.linked_deadline_item."""
# LOGGING
import logging

from django.db import models

from apps.deadlines.models import (DeadlineItem, LinkedDeadline,
                                   LinkedDeadlineFlag)
from apps.visums.models import LinkedCheck, LinkedSubCategory
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineItem(AbstractBaseModel):

    parent = models.ForeignKey(
        DeadlineItem, on_delete=models.CASCADE, related_name="deadline_item"
    )

    linked_deadline = models.ForeignKey(
        LinkedDeadline,
        on_delete=models.CASCADE,
        related_name="items",
        null=True,
        blank=True,
    )

    linked_sub_category = models.ForeignKey(
        LinkedSubCategory,
        on_delete=models.CASCADE,
        related_name="deadline_items",
        null=True,
        blank=True,
    )
    linked_check = models.ForeignKey(
        LinkedCheck,
        on_delete=models.CASCADE,
        related_name="deadline_items",
        null=True,
        blank=True,
    )
    flag = models.OneToOneField(
        LinkedDeadlineFlag,
        on_delete=models.CASCADE,
        related_name="deadline_item",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["parent__index"]

    @property
    def name(self) -> str:
        if self.is_deadline():
            return self.flag.parent.name

        if self.is_sub_category_deadline():
            return self.linked_sub_category.parent.name

        if self.is_check_deadline():
            return self.linked_check.parent.name

    def is_deadline(self):
        return self.parent.is_deadline()

    def is_sub_category_deadline(self):
        return self.parent.is_sub_category_deadline()

    def is_check_deadline(self):
        return self.parent.is_check_deadline()

    def is_checked(self) -> bool:
        if self.is_deadline():
            return self.flag.flag

        if self.is_sub_category_deadline():
            return self.linked_sub_category.is_checked()

        if self.is_check_deadline():
            return self.linked_check.get_value_type().is_checked()
