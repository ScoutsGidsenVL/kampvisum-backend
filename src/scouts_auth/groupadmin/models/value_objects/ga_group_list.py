from typing import List

from scouts_auth.groupadmin.models.value_objects import GaGroup
from scouts_auth.inuits.models import AbstractNonModel


class GaGroupList(AbstractNonModel):
    """List of groups returned by GA endpoint GET /groepen (GA: lijst van groepen van een lid)."""

    scouts_groups: List[GaGroup]

    class Meta:
        abstract = True

    def __init__(self, scouts_groups: List[GaGroup] = None):
        self.scouts_groups = sorted(scouts_groups, key=lambda group: group.number) if scouts_groups else []
