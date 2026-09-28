from django.db import models

from scouts_auth.inuits.models.fields import OptionalTextField
from scouts_auth.inuits.utils import TextUtils


class Translatable(models.Model):
    """Provides a translatable object label (field name: label)"""

    label = OptionalTextField("label")

    class Meta:
        abstract = True

    def has_label(self) -> bool:
        return TextUtils.is_non_empty(self.label)
