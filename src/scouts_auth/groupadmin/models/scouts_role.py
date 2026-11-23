from typing import List

from scouts_auth.auth.exceptions import ScoutsAuthException

from scouts_auth.groupadmin.models import (
    GaMemberFunction,
    GaFunctionCode,
    ScoutsGroup,
)
from scouts_auth.groupadmin.models.fields import GroupAdminIdField

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalDateTimeField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsRole(AbstractNonModel):
    group_admin_id = GroupAdminIdField()
    end = OptionalDateTimeField()
    scouts_group = GroupAdminIdField()
    code = OptionalCharField()
    description = OptionalCharField()

    is_leader: bool = False

    class Meta:
        managed = False

    @property
    def scouts_function_code(self) -> GaFunctionCode:
        return GaFunctionCode(code=self.code)

    def is_active_function(self) -> bool:
        return not self.end

    def is_leader_function(self) -> bool:
        return self.is_leader

    def is_section_leader_function(self) -> bool:
        return self.is_leader_function()

    def is_group_leader_function(self) -> bool:
        return self.scouts_function_code.is_group_leader()

    def is_district_commissioner_function(self) -> bool:
        return self.scouts_function_code.is_district_commissioner()

    def is_shire_president_function(self) -> bool:
        return self.scouts_function_code.is_shire_president()

    def get_role_name(self) -> str:
        if self.is_shire_president_function():
            return "role_shire_president"
        if self.is_district_commissioner_function():
            return "role_district_commissioner"
        if self.is_group_leader_function():
            return "role_group_leader"
        if self.is_section_leader_function():
            return "role_section_leader"
        return "role_regular_member"

    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id})"
            f"end({self.end})"
            f"code ({self.code})"
            f"description ({self.description})"
            f"scouts_group ({self.scouts_group})"
        )

    def to_descriptive_string(self):
        return f"{self.code} - {self.description}: {self.scouts_group}"

    @staticmethod
    def from_abstract_function(
        scouts_function=None,
        abstract_function: GaMemberFunction = None,
    ):
        if not abstract_function:
            raise ScoutsAuthException("Can't construct a ScoutsRole without an GaMemberFunction")

        scouts_function: ScoutsRole = scouts_function if scouts_function else ScoutsRole()

        scouts_function.group_admin_id = abstract_function.function
        scouts_function.end = abstract_function.end
        scouts_function.code = abstract_function.code
        scouts_function.description = abstract_function.description

        return scouts_function
