from typing import List


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.value_objects import (
    AbstractScoutsValue,
    AbstractScoutsLink,
    AbstractScoutsResponse,
)
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsMemberListMember(AbstractNonModel):
    """Partial member data captured in a member list from a call to /ledenlijst."""

    group_admin_id = OptionalGroupAdminIdField()
    index: int
    values: List[AbstractScoutsValue]
    links: List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        index: int = 0,
        values: List[AbstractScoutsValue] = None,
        links: List[AbstractScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.index = index
        self.values = values if values else []
        self.links = links if links else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id({}), index({}), values({}), links({})".format(
            self.group_admin_id,
            self.index,
            ", ".join(str(value)
                      for value in self.values) if self.values else "[]",
            ", ".join(str(link)
                      for link in self.links) if self.links else "[]",
        )


class AbstractScoutsMemberListResponse(AbstractScoutsResponse):
    """Class to capture data returned from a call to /ledenlijst."""

    members: List[AbstractScoutsMemberListMember]

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
        links: List[AbstractScoutsLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(
            ", ".join(str(member)
                      for member in self.members) if self.members else "[]"
        )
