"""scouts_auth.auth.inuits.mixins.audit_update_model_mixin."""

from django.db import models

from scouts_auth.inuits.mixins import UpdatedByModelMixin, UpdatedOnModelMixin
import scouts_auth.inuits.mixins as inuits_mixins


class AuditUpdateModelMixin(UpdatedOnModelMixin, UpdatedByModelMixin, models.Model):
    """Specifies by who and when the object was updated (field names: updated_by, updated_on)"""

    class Meta:
        abstract = True
