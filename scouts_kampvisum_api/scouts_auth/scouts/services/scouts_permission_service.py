# LOGGING
import logging
from datetime import datetime
from lib2to3.pgen2.token import EQUAL
from typing import List

import pytz
from django.conf import settings
from django.core.exceptions import PermissionDenied

from scouts_auth.auth.services import PermissionService
from scouts_auth.groupadmin.models import (
    AbstractScoutsFunction,
    AbstractScoutsFunctionDescription,
    AbstractScoutsGroup,
    ScoutsFunction,
    ScoutsGroup,
)
from scouts_auth.groupadmin.settings import GroupAdminSettings
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.utils import GlobalSettingsUtil

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
        # logger.debug(
        #     "SCOUTS AUTHORIZATION SERVICE: updating user authorizations", user=user
        # )

        is_admin = False
        allowed = False

        # Initialize authorizations we can derive from membership of a scouts group
        if user.has_role_administrator():
            is_admin = True
            user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.ADMINISTRATOR)

        # if scouts_group:
        for scouts_group in user.get_scouts_groups():
            is_shire_president = False
            is_district_commissioner = False
            is_group_leader = False
            is_section_leader = False

            if user.has_role_shire_president(scouts_group=scouts_group):
                is_shire_president = True
                allowed = True

            if user.has_role_district_commissioner(scouts_group=scouts_group):
                is_district_commissioner = True
                allowed = True

            if user.has_role_group_leader(scouts_group=scouts_group):
                is_group_leader = True
                allowed = True

            if user.has_role_section_leader(scouts_group=scouts_group):
                is_section_leader = True
                allowed = True

            if is_shire_president:
                user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.SHIRE_PRESIDENT)

            if is_district_commissioner:
                user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.DISTRICT_COMMISSIONER)

            if is_group_leader:
                user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.GROUP_LEADER)

            if is_section_leader:
                user = self.add_user_to_group(user=user, group_name=ScoutsPermissionService.SECTION_LEADER)

        if not allowed and not is_admin:
            logger.warn("Not allowed to retrieve data for group %s", scouts_group.group_admin_id, user=user)
            raise PermissionDenied()

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
