import logging

from django.db import models
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


class LinkedCategoryQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LinkedCategoryManager(models.Manager):
    """
    Loads LinkedSubCategory instances by their name, not their id.
    """

    def get_queryset(self):
        return LinkedCategoryQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        category = kwargs.get("category", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except:
                pass

        if category:
            try:
                return self.get_queryset().get(parent=category)
            except:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate LinkedCategory instance(s) with provided params (id: {}, category: {})".format(
                    pk, category
                )
            )
        return None
