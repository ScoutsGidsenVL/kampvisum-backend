from django.conf import settings
from django.db import models


class CreatedByModelMixin(models.Model):
    """Stores the user that created the object (field name: created_by)"""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Created by",
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
