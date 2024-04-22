"""scouts_auth.auth.inuits.mixins.updated_on_model_mixin."""

import django
from django.db import models


class UpdatedOnModelMixin(models.Model):
    """Stores the datetime when the object was updated (field name: updated_on)"""

    updated_on = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        abstract = True
