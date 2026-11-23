from typing import List

from django.conf import settings

from apps.groups.services import ScoutsSectionService

from scouts_auth.groupadmin.models import (
    GaProfileMember,
    GaGroup,
    ScoutsGroup,
    ScoutsUser,
)
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.scouts.services import ScoutsPermissionService, ScoutsUserSessionService

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserService:
    groupadmin = GroupAdminMemberService()
    permission_service = ScoutsPermissionService()
    section_service = ScoutsSectionService()
    session_service = ScoutsUserSessionService()

    def get_scouts_user(
        self, active_user: settings.AUTH_USER_MODEL, abstract_member: GaProfileMember
    ) -> settings.AUTH_USER_MODEL:
        # Clear any lingering data
        active_user.clear_data()

        # #######
        # 1. MEMBER PROFILE (rest-ga/lid/profiel)
        #
        # Get the member profile from groepsadmin
        #
        # This contains:
        # - basic user data (username, first_name, phone number, ...)
        # The functions in the profile aren't used: roles come from the responsibilities in step 2.
        # abstract_user: GaProfileMember = self.group_admin.get_member_profile(
        #     active_user=active_user)
        #
        # -- Already done by the authentication backend
        logger.debug(f"[AUTHENTICATION/AUTHORISATION] Constructing a ScoutsUser object", user=active_user)

        # #######
        # 2. GROUPS (rest-ga/groep)
        #
        # Get the list of scouts groups for which the user has rights
        #
        # This contains all the scouts groups the user is allowed to see
        # An GaGroup contains:
        # - The group's groepsnummer
        # - The group's name
        # - The user's responsibilities over the group (GA: verantwoordelijkheden), from which
        #   ScoutsUser derives the roles. No function call (rest-ga/functie) is needed for that.
        abstract_groups: List[GaGroup] = self.groupadmin.get_groups(active_user=active_user).scouts_groups
        user_groups = self.process_groups(abstract_groups=abstract_groups)

        if ScoutsUser.has_administrator_groups(user_groups=user_groups):
            from apps.visums.models import CampVisum

            groups = CampVisum.objects.get_queryset().get_linked_groups()
            for group in groups:
                # visums_campvisum.group holds the groepsnummer
                if group[0] not in [user_group.number for user_group in user_groups]:
                    admin_group = ScoutsGroup()

                    admin_group.number = group[0]
                    admin_group.name = group[1]

                    user_groups.append(admin_group)

        # #######
        # 3. PROCESS GROUPS
        for scouts_group in user_groups:
            active_user.add_scouts_group(scouts_group=scouts_group)

        logger.info(active_user.to_descriptive_string())

        logger.debug(f"[AUTHENTICATION/AUTHORISATION] Updating user authorisations", user=active_user)
        self.permission_service.update_user_authorizations(user=active_user)

        logger.debug(f"[AUTHENTICATION/AUTHORISATION] Setting up default scouts sections", user=active_user)
        self.section_service.setup_default_sections(user=active_user)

        logger.debug(f"[AUTHENTICATION/AUTHORISATION] ScoutsUser object initialised", user=active_user)

        return active_user

    def process_groups(self, abstract_groups: List[GaGroup]) -> List[ScoutsGroup]:
        return [ScoutsGroup.from_abstract_scouts_group(abstract_group=abstract_group) for abstract_group in abstract_groups]
