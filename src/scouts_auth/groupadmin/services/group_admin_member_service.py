from typing import List
from datetime import datetime

from django.conf import settings

from scouts_auth.groupadmin.models import (
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
    ) -> List[GaSearchMember]:
        """
        Searches for scouts members and applies some filters

        USAGE:
        - if group_group_admin_id is set, users will be filtered based on membership of that group
        - if include_inactive is False, only active members are returned (no oudleden)
        - if include_inactive is True, two separate GA calls are made: one for active members and one
          for oudleden (GA: oudleden=True). Oudleden are returned as GaSearchMember with inactive_member=True.
          Members appearing in both lists are treated as active.
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

        active_list: List[GaListMember] = self._fetch_all_list_members(
            active_user, term, group_group_admin_id, min_age, max_age, gender, function_ids, oudleden=False
        )

        logger.debug("GA returned %d active member(s) for search term %s", len(active_list), term)

        if not include_inactive:
            logger.debug(
                "Found %d member(s) for search term %s, group_admin_id %s, include_inactive %s, min_age %s, max_age %s and gender %s",
                len(active_list),
                term,
                group_group_admin_id,
                include_inactive,
                min_age,
                max_age,
                gender,
            )
            return [self._list_member_to_search_member(m) for m in active_list]

        active_ids = {m.group_admin_id for m in active_list}

        oudleden_list: List[GaListMember] = self._fetch_all_list_members(
            active_user, term, group_group_admin_id, min_age, max_age, gender, function_ids, oudleden=True
        )

        logger.debug("GA returned %d oudleden for search term %s", len(oudleden_list), term)

        all_members = active_list + [m for m in oudleden_list if m.group_admin_id not in active_ids]

        members = [self._list_member_to_search_member(m) for m in all_members]

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

    def _fetch_all_list_members(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str,
        group_group_admin_id: str,
        min_age: int,
        max_age: int,
        gender: str,
        function_ids: list,
        oudleden: bool,
    ) -> List[GaListMember]:
        response: GaListMemberPage = self.get_member_list_filtered(
            active_user, term, group_group_admin_id, min_age, max_age, gender,
            functies=function_ids, oudleden=oudleden,
        )
        if not response.members:
            return []
        members = list(response.members)
        while next_link := next((link for link in response.links if link.rel == "next"), None):
            # next_link.href points to the same filtered endpoint with offset query param
            response = self.get_member_list_filtered(
                active_user, term, group_group_admin_id, min_age, max_age, gender,
                next_url=next_link.href, functies=function_ids, oudleden=oudleden,
            )
            members.extend(response.members)
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
            inactive_member=not list_member.active_member,
            links=list_member.links,
        )
        member.gender = gender
        return member

