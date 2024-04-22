"""scouts_auth.auth.inuits.mixins.created_on_model_mixin."""

from django.db import models
from django.utils import timezone


class CreatedOnModelMixin(models.Model):
    """Stores the datetime when the object was created (field name: created_on)"""

    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
