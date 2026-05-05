from typing import List


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
    index: int
    values: List[GaValue]
    links: List[GaLink]
    active_member: bool

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        index: int = 0,
        values: List[GaValue] = None,
        links: List[GaLink] = None,
        active_member: bool = True,
    ):
        self.group_admin_id = group_admin_id
        self.index = index
        self.values = values if values else []
        self.links = links if links else []
        self.active_member = active_member

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id({}), index({}), values({}), links({})".format(
            self.group_admin_id,
            self.index,
            ", ".join(str(value) for value in self.values) if self.values else "[]",
            ", ".join(str(link) for link in self.links) if self.links else "[]",
        )


class GaListMemberPage(GaPage):
    """Paginated response from GA endpoint POST /ledenlijst/filter/stateless (GA: ledenlijst)."""

    members: List[GaListMember]

    class Meta:
        abstract = True

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        members: list = None,
        links: List[GaLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(
            ", ".join(str(member) for member in self.members) if self.members else "[]"
        )
