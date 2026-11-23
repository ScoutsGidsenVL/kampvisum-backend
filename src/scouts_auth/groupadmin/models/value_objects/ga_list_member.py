from typing import List, Optional


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.value_objects import (
    GaValue,
    GaLink,
    GaPage,
)
from scouts_auth.inuits.models import AbstractNonModel


class GaListMember(AbstractNonModel):
    """Partial member data returned by GA endpoint POST /ledenlijst/filter/stateless (GA: lid uit ledenlijst)."""

    group_admin_id = OptionalGroupAdminIdField()
    values: List[GaValue]

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        values: List[GaValue] = None,
        active_member: Optional[bool] = None,
    ):
        self.group_admin_id = group_admin_id
        self.values = values if values else []
        self.active_member = active_member

    @property
    def active_member(self) -> bool:
        # GA does not return the member status: the caller sets it based on the request (oudleden or not).
        # Fail loudly instead of silently treating the member as active or inactive.
        if self._active_member is None:
            raise ValueError(f"GaListMember {self.group_admin_id}: active_member was never set")
        return self._active_member

    @active_member.setter
    def active_member(self, value: Optional[bool]):
        # Set once only. getattr: __init__ calls this setter before _active_member exists.
        if getattr(self, "_active_member", None) is not None:
            raise ValueError(f"GaListMember {self.group_admin_id}: active_member was already set")
        self._active_member = value

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id({}), values({})".format(
            self.group_admin_id,
            ", ".join(str(value) for value in self.values) if self.values else "[]",
        )


class GaListMemberPage(GaPage):
    """Paginated response from GA endpoint POST /ledenlijst/filter/stateless (GA: ledenlijst)."""

    members: List[GaListMember]

    class Meta:
        abstract = True

    def __init__(self, members: list = None, links: List[GaLink] = None):
        self.members = members if members else []

        super().__init__(links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(
            ", ".join(str(member) for member in self.members) if self.members else "[]"
        )
