import pytz
from lib2to3.pgen2.token import EQUAL
from typing import List
from datetime import datetime

from django.conf import settings
from django.core.exceptions import PermissionDenied

from scouts_auth.auth.services import PermissionService

from scouts_auth.groupadmin.models import (
    GaGroup,
    ScoutsGroup,
    GaMemberFunction,
    GaFunctionDescription,
    ScoutsRole,
)
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.utils import GlobalSettingsUtil


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsPermissionService(PermissionService):
    USER = "role_user"
    SECTION_LEADER = "role_section_leader"
    GROUP_LEADER = "role_group_leader"
    DISTRICT_COMMISSIONER = "role_district_commissioner"
    SHIRE_PRESIDENT = "role_shire_president"
    ADMINISTRATOR = "role_administrator"

    known_roles = [
        USER,
        SECTION_LEADER,
        GROUP_LEADER,
        DISTRICT_COMMISSIONER,
        SHIRE_PRESIDENT,
        ADMINISTRATOR,
    ]

    def update_user_authorizations(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        """Determine the user's roles from their scouts groups and assign the
        corresponding Django auth groups.

        Raises PermissionDenied if the user has no valid role.
        """
        roles_needed = set()
        allowed = False

        if user.has_role_administrator():
            roles_needed.add(ScoutsPermissionService.ADMINISTRATOR)
            allowed = True

        scouts_groups = user.get_scouts_groups()

        # Each loop iterates scouts_groups just to find one role. The separate loops
        # with break are done to short-circuit per role
        # (stop checking groups once the role is found)
        for scouts_group in scouts_groups:
            if user.has_role_shire_president(scouts_group=scouts_group):
                roles_needed.add(ScoutsPermissionService.SHIRE_PRESIDENT)
                allowed = True
                break

        for scouts_group in scouts_groups:
            if user.has_role_district_commissioner(scouts_group=scouts_group):
                roles_needed.add(ScoutsPermissionService.DISTRICT_COMMISSIONER)
                allowed = True
                break

        for scouts_group in scouts_groups:
            if user.has_role_group_leader(scouts_group=scouts_group):
                roles_needed.add(ScoutsPermissionService.GROUP_LEADER)
                allowed = True
                break

        for scouts_group in scouts_groups:
            if user.has_role_section_leader(scouts_group=scouts_group):
                roles_needed.add(ScoutsPermissionService.SECTION_LEADER)
                allowed = True
                break

        if not allowed:
            logger.warning("User not allowed: no valid role found", user=user)
            raise PermissionDenied()

        # Assign each needed role exactly once
        for role in roles_needed:
            user = self.add_user_to_group(user=user, group_name=role)

        if GroupAdminSettings.is_debug():
            test_groups = GroupAdminSettings.get_test_groups()
            if any(group in user.get_group_names() for group in test_groups):
                logger.debug(
                    "User %s is member of a test group and DEBUG is set to True, adding user as administrator",
                    user.username,
                )
                GlobalSettingsUtil.is_test = True
                user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.ADMINISTRATOR)

        return user
