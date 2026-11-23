from typing import List


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    ListField,
)


class GaGroup(AbstractNonModel):
    """Models the scouts groups a user has rights to."""

    group_admin_id = OptionalGroupAdminIdField()
    number = OptionalCharField()
    name = OptionalCharField()
    child_groups = ListField()
    type = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        number: str = "",
        name: str = "",
        child_groups: List[str] = None,
        type: str = "",
    ):
        self.group_admin_id = group_admin_id
        self.number = number
        self.name = name
        self.child_groups = child_groups if child_groups else []
        self.type = type

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id({}), number({}), name({}), child_groups ({}), type({})".format(
            self.group_admin_id,
            self.number,
            self.name,
            ", ".join(group for group in self.child_groups),
            self.type,
        )
