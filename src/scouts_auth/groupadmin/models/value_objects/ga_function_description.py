from typing import List


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.value_objects import GaGrouping
from scouts_auth.inuits.models import AbstractNonModel


class GaFunctionDescription(AbstractNonModel):
    """
    An available function type in the GA catalog (GA: functie).
    Describes what functions a member can hold. Only used to search for leaders.
    """

    group_admin_id = OptionalGroupAdminIdField()

    # Declare as foreign keys in concrete subclasses
    groupings: List[GaGrouping] = []

    class Meta:
        abstract = True

    def __init__(self, group_admin_id: str = None, groupings: List[GaGrouping] = None):
        self.group_admin_id = group_admin_id
        self.groupings = groupings if groupings else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id ({}), groupings({})".format(
            self.group_admin_id,
            ", ".join(str(grouping) for grouping in self.groupings) if self.groupings else "[]",
        )
