from typing import List

from scouts_auth.groupadmin.models.value_objects import GaGroup, GaLink
from scouts_auth.inuits.models import AbstractNonModel


class GaGroupList(AbstractNonModel):
    """List of groups returned by GA endpoint GET /groepen (GA: lijst van groepen van een lid)."""

    scouts_groups: List[GaGroup]
    links: List[GaLink]

    class Meta:
        abstract = True

    def __init__(self, scouts_groups: List[GaGroup] = None, links: List[GaLink] = None):
        self.scouts_groups = scouts_groups.sort(key=lambda group: group.group_admin_id) if scouts_groups else []
        self.links = links if links else []
