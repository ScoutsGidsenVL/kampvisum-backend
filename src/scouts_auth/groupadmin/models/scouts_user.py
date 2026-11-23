from typing import List, Tuple

from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager

from scouts_auth.auth.exceptions import InvalidArgumentException, ScoutsAuthException
from scouts_auth.auth.models import User
from scouts_auth.groupadmin.models import (
    GaProfileMember,
    ScoutsGroup,
    ScoutsToken,
)
from scouts_auth.groupadmin.models.scouts_group import (
    RESPONSIBILITY_GENERAL,
    RESPONSIBILITY_LEADER,
    RESPONSIBILITY_REGIONAL,
)
from scouts_auth.groupadmin.models.fields import GroupAdminIdField
from scouts_auth.groupadmin.settings import GroupAdminSettings
from scouts_auth.inuits.utils import SettingsHelper


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserManager(UserManager):
    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        username = kwargs.get("username", None)
        group_admin_id = kwargs.get("group_admin_id", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if username:
            try:
                return self.get_by_natural_key(username)
            except Exception:
                pass

        if group_admin_id:
            try:
                return self.get_queryset().get(group_admin_id=group_admin_id)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsGroup instance(s) with the provided params: (id: {}, group_admin_id: {})".format(
                    pk,
                    group_admin_id,
                )
            )

        return None

    def get_by_natural_key(self, username):
        logger.trace(
            "GET BY NATURAL KEY %s: (username: %s (%s))",
            "ScoutsUser",
            username,
            type(username).__name__,
        )

        return super().get_by_natural_key(username)


class ScoutsUser(User):
    objects = ScoutsUserManager()

    group_admin_id: str = GroupAdminIdField()

    _scouts_groups: List[ScoutsGroup] = []

    #
    # The active access token, provided by group admin oidc
    #
    _access_token: ScoutsToken = None

    def __init__(self, *args, **kwargs):
        self._scouts_groups = []
        self._access_token = None

        super().__init__(*args, **kwargs)

    @property
    def access_token(self) -> ScoutsToken:
        return self._access_token.access_token if self._access_token else None

    @access_token.setter
    def access_token(self, access_token: ScoutsToken):
        if not isinstance(access_token, ScoutsToken):
            raise ScoutsAuthException(
                f"[{self.username}] ScoutsUser only accepts a ScoutsToken instance for access token, not {access_token.__class__.__name__}"
            )

        self._access_token = access_token

    def clear_data(self):
        self._scouts_groups.clear()

    def add_scouts_group(self, scouts_group: ScoutsGroup):
        if not isinstance(self._scouts_groups, List):
            self._scouts_groups = []

        if scouts_group.number not in self.get_scouts_group_names():
            self._scouts_groups.append(scouts_group)
            self._scouts_groups.sort(key=lambda x: x.number)

    def get_scouts_group(self, group_number: str, raise_error: bool = False) -> ScoutsGroup:
        for scouts_group in self._scouts_groups:
            if scouts_group.number == group_number:
                return scouts_group

        if raise_error:
            raise InvalidArgumentException(f"[{self.username}] This user doesn't have access to group {group_number}")

        return None

    def get_scouts_groups(self) -> List[ScoutsGroup]:
        return self._scouts_groups

    def get_scouts_group_names(self) -> List[str]:
        return [group.number for group in self._scouts_groups]
    #
    # ROLES
    #
    # Roles are derived from the responsibilities GA returns per group in rest-ga/groep
    # (GA: verantwoordelijkheden). GA computes those from the active functions of the user, see the
    # tables verantwoordelijkheid, selectie and selectie_groep in the groepsadmin database:
    # - "leiding": a leader function (tak 10) in the group itself
    # - "algemeen": GRL, AGRL, GRLP in a regular group, DC, ADC in a district, GV, GB, GC in a gouw
    # - "regionaal": DC, ADC over the groups in their district, the gouwbureau and its adjuncts
    #   over the districts and groups in their gouw
    #
    ROLE_SECTION_LEADER = "role_section_leader"
    ROLE_GROUP_LEADER = "role_group_leader"
    ROLE_DISTRICT_COMMISSIONER = "role_district_commissioner"
    ROLE_REGIONAL = "role_regional"

    def _resolve_group(self, scouts_group: ScoutsGroup = None, group_number: str = None) -> ScoutsGroup:
        if scouts_group:
            return scouts_group
        if not group_number:
            raise InvalidArgumentException("Can't determine a role without a group or group number")
        return self.get_scouts_group(group_number=group_number)

    def _has_role_in_any_group(self, has_role) -> bool:
        return any(has_role(scouts_group=scouts_group) for scouts_group in self._scouts_groups)

    def _get_role_groups(self, has_role) -> List[ScoutsGroup]:
        return [scouts_group for scouts_group in self._scouts_groups if has_role(scouts_group=scouts_group)]

    def get_roles_for_group(self, scouts_group: ScoutsGroup = None, group_number: str = None) -> List[str]:
        if not scouts_group and not group_number:
            raise InvalidArgumentException("Can't determine roles for group without a scouts group or group number")

        scouts_group = self._resolve_group(scouts_group=scouts_group, group_number=group_number)
        if not scouts_group:
            return []

        roles: List[str] = []
        if self.has_role_regional(scouts_group=scouts_group):
            roles.append(ScoutsUser.ROLE_REGIONAL)
        if self.has_role_district_commissioner(scouts_group=scouts_group):
            roles.append(ScoutsUser.ROLE_DISTRICT_COMMISSIONER)
        if self.has_role_group_leader(scouts_group=scouts_group):
            roles.append(ScoutsUser.ROLE_GROUP_LEADER)
        if self.has_role_section_leader(scouts_group=scouts_group):
            roles.append(ScoutsUser.ROLE_SECTION_LEADER)

        return roles

    def has_role_leader(
        self, scouts_group: ScoutsGroup = None, group_number: str = None, ignore_group: bool = False
    ) -> bool:
        """Determines if the user is a leader in the specified group (responsibility "leiding")"""
        if ignore_group:
            return self._has_role_in_any_group(self.has_role_leader)

        scouts_group = self._resolve_group(scouts_group=scouts_group, group_number=group_number)
        return bool(scouts_group) and scouts_group.has_responsibility(RESPONSIBILITY_LEADER)

    def has_role_section_leader(
        self, scouts_group: ScoutsGroup = None, group_number: str = None, ignore_group: bool = False
    ) -> bool:
        """Determines if the user is a section leader in the specified group (responsibility "leiding")"""
        return self.has_role_leader(scouts_group=scouts_group, group_number=group_number, ignore_group=ignore_group)

    def has_role_group_leader(
        self, scouts_group: ScoutsGroup = None, group_number: str = None, ignore_group: bool = False
    ) -> bool:
        """
        Determines if the user is a group leader in the specified group:
        responsibility "algemeen" on a regular group (not a district or gouw)
        """
        if ignore_group:
            return self._has_role_in_any_group(self.has_role_group_leader)

        scouts_group = self._resolve_group(scouts_group=scouts_group, group_number=group_number)
        return (
            bool(scouts_group)
            and scouts_group.is_regular_group()
            and scouts_group.has_responsibility(RESPONSIBILITY_GENERAL)
        )

    def has_role_district_commissioner(
        self, scouts_group: ScoutsGroup = None, group_number: str = None, ignore_group: bool = False
    ) -> bool:
        """
        Determines if the user is a district commissioner for the specified group.

        A DC has responsibility "algemeen" on the district itself and "regionaal" on the groups in
        that district. "regionaal" alone isn't enough, because the gouw has it on the same groups.
        """
        if ignore_group:
            return self._has_role_in_any_group(self.has_role_district_commissioner)

        scouts_group = self._resolve_group(scouts_group=scouts_group, group_number=group_number)
        if not scouts_group:
            return False

        dc_district_prefixes = [
            group.district_prefix()
            for group in self._scouts_groups
            if group.is_district() and group.has_responsibility(RESPONSIBILITY_GENERAL)
        ]

        if scouts_group.is_district():
            return scouts_group.district_prefix() in dc_district_prefixes

        return (
            scouts_group.district_prefix() in dc_district_prefixes
            and scouts_group.has_responsibility(RESPONSIBILITY_REGIONAL)
        )

    def has_role_regional(
        self, scouts_group: ScoutsGroup = None, group_number: str = None, ignore_group: bool = False
    ) -> bool:
        """Determines if the user has regional (read) access to the specified group (responsibility "regionaal")"""
        if ignore_group:
            return self._has_role_in_any_group(self.has_role_regional)

        scouts_group = self._resolve_group(scouts_group=scouts_group, group_number=group_number)
        return bool(scouts_group) and scouts_group.has_responsibility(RESPONSIBILITY_REGIONAL)

    def has_any_role(self, scouts_group: ScoutsGroup) -> bool:
        return len(self.get_roles_for_group(scouts_group=scouts_group)) > 0

    def get_scouts_leader_groups(self) -> List[ScoutsGroup]:
        """The groups in which the user has a camp visum role, or all groups for an administrator"""
        if self.has_role_administrator():
            return self._scouts_groups
        return self._get_role_groups(self.has_any_role)

    def get_scouts_leader_group_names(self) -> List[str]:
        return [scouts_group.number for scouts_group in self.get_scouts_leader_groups()]

    def get_scouts_section_leader_groups(self) -> List[ScoutsGroup]:
        return self._get_role_groups(self.has_role_section_leader)

    def get_scouts_group_leader_groups(self) -> List[ScoutsGroup]:
        return self._get_role_groups(self.has_role_group_leader)

    def get_scouts_district_commissioner_groups(self) -> List[ScoutsGroup]:
        return self._get_role_groups(self.has_role_district_commissioner)

    def get_scouts_district_commissioner_group_ids_and_names(self) -> List[Tuple[str, str]]:
        return [(group.number, group.name) for group in self.get_scouts_district_commissioner_groups()]

    def get_scouts_regional_groups(self) -> List[ScoutsGroup]:
        return self._get_role_groups(self.has_role_regional)

    def get_scouts_regional_group_ids_and_names(self) -> List[Tuple[str, str]]:
        return [(group.number, group.name) for group in self.get_scouts_regional_groups()]

    def has_role_administrator(self) -> bool:
        """
        Determines if the user is an administrative worker based on membership of an administrative group
        """
        if ScoutsUser.has_administrator_groups(user_groups=self.get_scouts_groups()):
            return True
        return False

    @staticmethod
    def has_administrator_groups(user_groups: List[ScoutsGroup]):
        return any(
            name in [user_group.number for user_group in user_groups]
            for name in GroupAdminSettings.get_administrator_groups()
        )


    def __str__(self):
        return (
            f"group_admin_id ({self.group_admin_id}), "
            f"scouts_groups ({', '.join(str(group) for group in self._scouts_groups) if self._scouts_groups else '[]'})"
        )

    def to_descriptive_string(self):
        auth_groups = self.groups.all()
        permissions = self.get_all_permissions()

        def numbers(scouts_groups: List[ScoutsGroup]) -> str:
            return ", ".join(group.number for group in scouts_groups) if scouts_groups else "None"

        lines = [
            ("username", self.username),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email),
            ("group_admin_id", self.group_admin_id),
            ("IS_ACTIVE", self.is_active),
            ("IS_AUTHENTICATED", self.is_authenticated),
            ("PERMISSIONS", ", ".join(permissions) if permissions else "None"),
            ("AUTH GROUPS", ", ".join(group.name for group in auth_groups) if auth_groups else "None"),
            (
                "RESPONSIBILITIES",
                ", ".join(f"{group.number} {group.responsibilities}" for group in self._scouts_groups)
                if self._scouts_groups
                else "None",
            ),
            ("SCOUTS LEADER GROUPS", numbers(self.get_scouts_leader_groups())),
            ("ADMINISTRATOR ?", self.has_role_administrator()),
            ("REGIONAL", numbers(self.get_scouts_regional_groups())),
            ("DISTRICT COMMISSIONER", numbers(self.get_scouts_district_commissioner_groups())),
            ("GROUP LEADER", numbers(self.get_scouts_group_leader_groups())),
            ("SECTION LEADER", numbers(self.get_scouts_section_leader_groups())),
            ("KNOWN_ADMIN_GROUPS", SettingsHelper.get_list("KNOWN_ADMIN_GROUPS")),
            ("KNOWN_TEST_GROUPS", SettingsHelper.get_list("KNOWN_TEST_GROUPS")),
            ("DEBUG", SettingsHelper.get_bool("DEBUG")),
            ("IS_ACCEPTANCE", SettingsHelper.get_bool("IS_ACCEPTANCE")),
            ("Is test ?", GroupAdminSettings.is_test()),
        ]
        separator = "-" * 120

        return "\n".join(
            ["", separator, "USER INFO", separator] + [f"{label:<24}: {value}" for label, value in lines] + [separator]
        )

    @staticmethod
    def from_abstract_member(user=None, abstract_member: GaProfileMember = None):
        if not abstract_member:
            raise ValidationError("Can't construct a ScoutsUser without an GaProfileMember")

        user = user if user else ScoutsUser()

        user.id = abstract_member.group_admin_id
        user.group_admin_id = abstract_member.group_admin_id
        user.first_name = abstract_member.first_name if abstract_member.first_name else ""
        user.last_name = abstract_member.last_name if abstract_member.last_name else ""
        user.email = abstract_member.email

        return user
