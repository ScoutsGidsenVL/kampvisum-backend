import typing as tp

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsGroup
from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink
from scouts_auth.inuits.models import AbstractNonModel


class AbstractScoutsGroupListResponse(AbstractNonModel):

    scouts_groups: tp.List[AbstractScoutsGroup]
    links: tp.List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(self, scouts_groups: tp.List[AbstractScoutsGroup] = None, links: tp.List[AbstractScoutsLink] = None):
        self.scouts_groups = scouts_groups.sort(key=lambda group: group.group_admin_id) if scouts_groups else []
        self.links = links if links else []
