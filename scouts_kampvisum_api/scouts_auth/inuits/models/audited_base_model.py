from scouts_auth.inuits.mixins import AuditCreateModelMixin
from scouts_auth.inuits.mixins import AuditUpdateModelMixin
from scouts_auth.inuits.models import AbstractBaseModel


class AuditedBaseModel(AbstractBaseModel, AuditCreateModelMixin, AuditUpdateModelMixin):
    """Abstract base models that logs create and update events for time and user."""

    class Meta:
        abstract = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
