from django.db import models

from apps.visums.models import Category, LinkedCategorySet
from apps.visums.models.enums import CheckState
from apps.visums.managers import LinkedCategoryManager

from scouts_auth.inuits.models import AbstractBaseModel


class LinkedCategory(AbstractBaseModel):

    objects = LinkedCategoryManager()

    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    category_set = models.ForeignKey(
        LinkedCategorySet, on_delete=models.CASCADE, related_name="categories"
    )

    class Meta:
        ordering = ["parent__index"]

    def is_checked(self) -> CheckState:
        for sub_category in self.sub_categories.all():
            if not sub_category.is_checked():
                return CheckState.UNCHECKED
        return CheckState.CHECKED
