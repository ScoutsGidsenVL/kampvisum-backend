from typing import List
from datetime import date, datetime, timedelta

from django.conf import settings

from scouts_auth.groupadmin.models import (
    GaProfileMember,
    GaSearchMember,
    GaListMember,
    GaListMemberPage,
    GaFunctionDescription,
)
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.groupadmin.services.group_admin import (
    GA_COL_FIRST_NAME,
    GA_COL_LAST_NAME,
    GA_COL_BIRTH_DATE,
    GA_COL_GENDER,
    GA_COL_EMAIL,
    GA_COL_PHONE,
)
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.models import Gender, GenderHelper

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GroupAdminMemberService(GroupAdmin):
    def search_member_filtered(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str,
        group_group_admin_id: str = None,
        include_inactive: bool = True,
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
        leader: bool = False,
    ) -> List[GaProfileMember]:
        """
        Searches for scouts members and applies some filters

        USAGE:
        - if group_group_admin_id is set, users will be filtered based on membership of that group
        - if include_inactive is False, then members who were last active since the ACTIVITY_EPOCH setting are excluded
        - if min_age, max_age or gender are set, members will be filtered based on the the year of their birth and gender.
        """
        function_ids = None
        if leader:
            function_descriptions: List[GaFunctionDescription] = self.get_function_descriptions(
                active_user=active_user
            ).function_descriptions

            function_ids = [
                fd.group_admin_id
                for fd in function_descriptions
                if any(g.name == GroupAdminSettings.get_leadership_status_identifier() for g in fd.groupings)
            ]

        response: GaListMemberPage = self.get_member_list_filtered(
            active_user, term, group_group_admin_id, min_age, max_age, gender,
            functies=function_ids, include_inactive=include_inactive,
        )
        if len(response.members) == 0:
            return []

        all_members: List[GaListMember] = []
        all_members.extend(response.members)
        if len(response.members) == 50:
            offset = 50
            while len(response.members) == 50:
                response = self.get_member_list_filtered(
                    active_user, term, group_group_admin_id, min_age, max_age, gender, offset,
                    functies=function_ids, include_inactive=include_inactive,
                )
                all_members.extend(response.members)
                offset += 50

        logger.debug(
            "GA returned a list of %d member(s) for search term %s",
            len(all_members),
            term,
        )

        if not include_inactive:
            logger.debug(
                "Found %d member(s) for search term %s, group_admin_id %s, include_inactive %s, min_age %s, max_age %s and gender %s",
                len(all_members),
                term,
                group_group_admin_id,
                include_inactive,
                min_age,
                max_age,
                gender,
            )
            return [self._list_member_to_search_member(m) for m in all_members]

        current_datetime: datetime = datetime.now()
        activity_epoch: date = self._calculate_activity_epoch_date(
            current_datetime, GroupAdminSettings.get_activity_epoch()
        )

        members: List[GaProfileMember] = []
        for response_member in all_members:
            member: GaProfileMember = self.get_member_info(
                active_user=active_user, group_admin_id=response_member.group_admin_id
            )
            if not self._filter_by_activity(
                member=member,
                include_inactive=include_inactive,
                current_datetime=current_datetime,
                activity_epoch=activity_epoch,
            ):
                continue
            members.append(member)

        logger.debug(
            "Found %d member(s) for search term %s, group_admin_id %s, include_inactive %s, min_age %s, max_age %s and gender %s",
            len(members),
            term,
            group_group_admin_id,
            include_inactive,
            min_age,
            max_age,
            gender,
        )

        return members

    def _list_member_to_search_member(self, list_member: GaListMember) -> GaSearchMember:
        values = {v.key: v.value for v in list_member.values}
        birth_date_str = values.get(GA_COL_BIRTH_DATE, "")
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date() if birth_date_str else None
        gender = GenderHelper.parse_gender(values.get(GA_COL_GENDER, ""))
        member = GaSearchMember(
            group_admin_id=list_member.group_admin_id,
            first_name=values.get(GA_COL_FIRST_NAME, ""),
            last_name=values.get(GA_COL_LAST_NAME, ""),
            birth_date=birth_date,
            email=values.get(GA_COL_EMAIL, ""),
            phone_number=values.get(GA_COL_PHONE, ""),
            links=list_member.links,
        )
        member.gender = gender
        return member

    def _calculate_activity_epoch_date(self, current_date: datetime, number_of_years: int) -> date:
        if number_of_years == 0:
            return datetime.fromtimestamp(0).date()

        return (current_date - timedelta(days=number_of_years * 365)).date()

    def _filter_by_group(
        self,
        member: GaProfileMember,
        group_group_admin_id: str,
    ) -> bool:
        member_in_group = False

        for function in member.functions:
            if function.scouts_group.group_admin_id == group_group_admin_id:
                logger.debug(
                    "INCLUDE: Member %s %s (%s) is in group %s",
                    member.first_name,
                    member.last_name,
                    member.email,
                    group_group_admin_id,
                )
                member_in_group = True
                break

        if not member_in_group:
            logger.debug(
                "EXCLUDE: Member %s %s (%s) is not in group %s",
                member.first_name,
                member.last_name,
                member.email,
                group_group_admin_id,
            )

        return member_in_group

    # @TODO code copied from scouts_authorization_service - should be abstracted
    def _filter_by_leadership(
        self,
        member: GaProfileMember,
        group_group_admin_id: str,
        function_descriptions: List[GaFunctionDescription],
        leader: bool = True,
        active_leader: bool = False,
    ) -> bool:
        logger.debug(
            "Found %d functions in member profile of %s %s (%s) and %d function descriptions",
            len(member.functions),
            member.first_name,
            member.last_name,
            member.email,
            len(function_descriptions),
        )
        function_activities: List[tuple] = []
        for member_function in member.functions:
            if member_function.scouts_group.group_admin_id == group_group_admin_id:
                for function_description in function_descriptions:
                    if function_description.group_admin_id == member_function.function:
                        for grouping in function_description.groupings:
                            if grouping.name == GroupAdminSettings.get_leadership_status_identifier():
                                if member_function.end:
                                    function_activities.append((True, False))
                                else:
                                    function_activities.append((True, True))

        leader_in_group = False
        active_leader_in_group = False
        for leader_function, active_leader_function in function_activities:
            if leader_function:
                leader_in_group = True
            if active_leader_function:
                leader_in_group = True
                active_leader_in_group = True

                break

        if leader_in_group:
            if active_leader:
                if active_leader_in_group:
                    logger.debug(
                        "INCLUDE: Member %s %s (%s) is an active leader in group %s",
                        member.first_name,
                        member.last_name,
                        member.email,
                        group_group_admin_id,
                    )
                    return True
                else:
                    logger.debug(
                        "EXCLUDE: Member %s %s (%s) is not an active leader in group %s",
                        member.first_name,
                        member.last_name,
                        member.email,
                        group_group_admin_id,
                    )
                    return False

            logger.debug(
                "INCLUDE: Member %s %s (%s) is a leader in group %s",
                member.first_name,
                member.last_name,
                member.email,
                group_group_admin_id,
            )
            return True
        else:
            logger.debug(
                "EXCLUDE: Member %s %s (%s) is not a leader in group %s",
                member.first_name,
                member.last_name,
                member.email,
                group_group_admin_id,
            )
            return False

    def _filter_by_activity(
        self,
        member: GaProfileMember,
        include_inactive: bool,
        current_datetime: date,
        activity_epoch: date,
    ) -> bool:
        for function in member.functions:
            active = not function.end
            if active:
                logger.debug(
                    "INCLUDE: Member %s %s (%s) has at least 1 active function",
                    member.first_name,
                    member.last_name,
                    member.email,
                )
                return True

        if include_inactive:
            for function in member.functions:
                if function.end and activity_epoch < function.end.date():
                    logger.debug(
                        "INCLUDE: Member %s %s (%s) is inactive, but include_inactive is set to True, including",
                        member.first_name,
                        member.last_name,
                        member.email,
                    )
                    member.inactive_member = (
                        True  # This can only be set after all functions have been checked for their activity.
                    )
                    return True

        logger.debug(
            "EXCLUDE: Member %s %s (%s) has been inactive for more than %d years",
            member.first_name,
            member.last_name,
            member.email,
            current_datetime.date().year - activity_epoch.year,
        )
        return False

    def _filter_by_age(
        self,
        member: GaProfileMember,
        min_age: int = None,
        max_age: int = None,
    ) -> bool:
        older_than_min_age = True
        younger_than_max_age = True

        delta = datetime.now().date().year - member.birth_date.year
        if min_age >= 0:
            if delta < min_age:
                older_than_min_age = False
        if max_age >= 0:
            if delta > max_age:
                younger_than_max_age = False

        if older_than_min_age and younger_than_max_age:
            logger.debug(
                "INCLUDE: Member %s %s (%s) is in the desired age range (%s - %s)",
                member.first_name,
                member.last_name,
                member.email,
                min_age,
                max_age,
            )
            return True
        else:
            logger.debug(
                "EXCLUDE: Member %s %s (%s) does not match the desired age range (%s - %s)",
                member.first_name,
                member.last_name,
                member.email,
                min_age,
                max_age,
            )

        return False

    def _filter_by_gender(self, member: GaProfileMember, gender) -> bool:
        if isinstance(gender, str):
            gender = GenderHelper.parse_gender(gender)

        if not member.has_gender():
            logger.debug("INCLUDE: A gender filter was set, but the GA member doesn't provide gender info")
            return True

        if member.gender == gender:
            logger.debug(
                "INCLUDE: Member %s %s (%s) has the requested gender %s",
                member.first_name,
                member.last_name,
                member.email,
                gender,
            )
            return True

        return False
