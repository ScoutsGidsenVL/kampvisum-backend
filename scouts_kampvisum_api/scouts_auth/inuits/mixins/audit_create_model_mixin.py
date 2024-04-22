"""scouts_auth.auth.inuits.mixins.audit_create_model_mixin."""

from django.db import models


# import scouts_auth.inuits.mixins as inuits_mixins

# from scouts_auth.inuits.mixins import CreatedByModelMixin, CreatedOnModelMixin
from scouts_auth.inuits.mixins.created_by_model_mixin import CreatedByModelMixin
from scouts_auth.inuits.mixins.created_on_model_mixin import CreatedOnModelMixin


class AuditCreateModelMixin(CreatedOnModelMixin, CreatedByModelMixin, models.Model):
    """Specifies by who and when the object was created (field names: created_by, created_on)"""

    class Meta:
        abstract = True
