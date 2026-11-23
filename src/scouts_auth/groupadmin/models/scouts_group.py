from typing import List

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import GaGroup
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.models import AbstractNonModel, Gender
from scouts_auth.inuits.models.fields import OptionalCharField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


# Responsibilities GA returns per group in rest-ga/groep (GA: verantwoordelijkheden).
# See the tables verantwoordelijkheid and selectie_groep in the groepsadmin database.
RESPONSIBILITY_LEADER = "leiding"
RESPONSIBILITY_GENERAL = "algemeen"
RESPONSIBILITY_REGIONAL = "regionaal"


class ScoutsGroup(AbstractNonModel):
    """
    A scouts group the user has access to, identified by its groepsnummer (e.g. X9010G).

    The last character of the groepsnummer gives the kind of group, the same convention GA uses:
    D is a district (e.g. X1200D), P is a gouw (e.g. X1000P), anything else is a regular group.
    The first 3 characters identify the district, the first 2 the gouw.
    """

    number = OptionalCharField()
    name = OptionalCharField()
    type = OptionalCharField()
    responsibilities: List[str] = None

    class Meta:
        managed = False

    def __init__(
        self,
        number: str = None,
        name: str = None,
        type: str = None,
        responsibilities: List[str] = None,
    ):
        self.number = number
        self.name = name
        self.type = type
        self.responsibilities = responsibilities if responsibilities else []

    def has_responsibility(self, responsibility: str) -> bool:
        return bool(self.responsibilities) and responsibility in self.responsibilities

    def is_district(self) -> bool:
        return bool(self.number) and self.number.upper().endswith("D")

    def is_shire(self) -> bool:
        return bool(self.number) and self.number.upper().endswith("P")

    def is_regular_group(self) -> bool:
        return bool(self.number) and not self.is_district() and not self.is_shire()

    def district_prefix(self) -> str:
        return self.number.upper()[:3] if self.number else ""

    @property
    def gender(self) -> Gender:
        identifier = self.number.upper().strip()[-1]
        if identifier == GroupAdminSettings().get_group_gender_identifier_male():
            return Gender.MALE
        if identifier == GroupAdminSettings.get_group_gender_identifier_female():
            return Gender.FEMALE
        return Gender.MIXED

    @property
    def full_name(self):
        return "{} {}".format(self.name, self.number)

    def is_admin_group(self) -> bool:
        return self.number in GroupAdminSettings.get_administrator_groups()

    def __str__(self):
        return (
            f"number ({self.number}), "
            f"name ({self.name}), "
            f"responsibilities ({self.responsibilities}), "
            f"type ({self.type})"
        )

    def __key__(self):
        return (self.number,)

    def __hash__(self):
        return hash(self.__key__())

    def __eq__(self, other):
        if isinstance(other, ScoutsGroup):
            return self.__hash__() == other.__hash__()
        return NotImplemented

    @staticmethod
    def from_abstract_scouts_group(scouts_group=None, abstract_group: GaGroup = None):
        if not abstract_group:
            raise ScoutsAuthException("Can't construct a ScoutsGroup without an GaGroup")

        scouts_group = scouts_group if scouts_group else ScoutsGroup()

        scouts_group.number = abstract_group.number
        scouts_group.name = abstract_group.name
        scouts_group.type = abstract_group.type
        scouts_group.responsibilities = list(abstract_group.responsibilities or [])

        return scouts_group
