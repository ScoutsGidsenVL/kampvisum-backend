import requests

from django.conf import settings
from django.http import Http404
from django.utils import timezone

# from drf_yasg.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    GaFunctionDescriptionList,
    GaGroup,
    GaGroupList,
    GaProfileMember,
    GaListMemberPage,
)
from scouts_auth.groupadmin.serializers import (
    GaFunctionDescriptionListSerializer,
    GaGroupSerializer,
    GaGroupListSerializer,
    GaListMemberPageSerializer,
    GaMemberSerializer,
)

from scouts_auth.groupadmin.settings import GroupAdminSettings

# Fully qualified Java class names used as keys in /ledenlijst/filter/stateless waarden dict
GA_COL_FIRST_NAME = "be.vvksm.groepsadmin.model.column.VoornaamColumn"
GA_COL_LAST_NAME = "be.vvksm.groepsadmin.model.column.AchternaamColumn"
GA_COL_BIRTH_DATE = "be.vvksm.groepsadmin.model.column.GeboorteDatumColumn"
GA_COL_GENDER = "be.vvksm.groepsadmin.model.column.GeslachtColumn"
GA_COL_EMAIL = "be.vvksm.groepsadmin.model.column.EmailColumn"
GA_COL_PHONE = "be.vvksm.groepsadmin.model.column.GsmColumn"
GA_COL_FUNCTIONS = "be.vvksm.groepsadmin.model.column.VVKSMFunktiesColumn"
GA_COL_STREET_NAME = "be.vvksm.groepsadmin.model.column.StraatnaamColumn"
GA_COL_STREET_NUMBER = "be.vvksm.groepsadmin.model.column.StraatnummerColumn"
GA_COL_BUS = "be.vvksm.groepsadmin.model.column.BusColumn"
GA_COL_POSTAL_CODE = "be.vvksm.groepsadmin.model.column.PostcodeColumn"
GA_COL_CITY = "be.vvksm.groepsadmin.model.column.GemeentenaamColumn"

# Timeout tuple for requests calls to the Groepsadmin, in seconds:
# First value: connect: max time to establish the TCP/TLS connection to the GA server.
#   Fails fast with ConnectTimeout when the GA is unreachable.
# Second value: read: max time to wait for the next bytes from the GA once connected
#   (per read, not for the whole response).
GA_TIMEOUT = (15, 15 * 60)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GroupAdmin:
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    url_groups = GroupAdminSettings.get_group_admin_group_endpoint()
    url_group = GroupAdminSettings.get_group_admin_group_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie
    url_functions = GroupAdminSettings.get_group_admin_functions_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    url_member_profile = GroupAdminSettings.get_group_admin_profile_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst/filter/stateless
    url_member_list_filtered = GroupAdminSettings.get_group_admin_member_list_filtered_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    url_member_info = GroupAdminSettings.get_group_admin_member_detail_endpoint() + "/{}"

    def post(self, endpoint: str, payload: dict, active_user: settings.AUTH_USER_MODEL = None) -> str:
        """Post the payload to the specified GA endpoint and returns the response as json_data."""
        # logger.debug(
        #     f"GA: Posting data to endpoint {endpoint}", user=active_user)
        try:
            if active_user:
                now = timezone.now()
                response = requests.post(
                    endpoint,
                    headers={
                        "Authorization": f"Bearer {active_user.access_token}",
                    },
                    json=payload,
                    timeout=GA_TIMEOUT,
                )
                logger.timing(
                    start=now,
                    method="POST",
                    endpoint=endpoint.replace(GroupAdminSettings.get_group_admin_base_url(), ""),
                    user=active_user,
                )
            else:
                response = requests.post(endpoint, data=payload, timeout=GA_TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            logger.warn(payload)
            logger.warn(response.text)
            if error.response.status_code == 404:
                raise Http404(f"404 - Unable to post to endpoint {endpoint} with payload {payload}")
            raise error

        return response.json()

    def get(self, endpoint: str, active_user: settings.AUTH_USER_MODEL):
        """Makes a request to the GA with the given url and returns the response as json_data."""
        # logger.debug(f"GA: Fetching data from endpoint {endpoint}")
        try:
            now = timezone.now()
            response = requests.get(
                endpoint,
                headers={"Authorization": f"Bearer {active_user.access_token}"},
                timeout=GA_TIMEOUT,
            )
            logger.timing(
                start=now,
                endpoint=endpoint.replace(GroupAdminSettings.get_group_admin_base_url(), ""),
                user=active_user,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404(f"404 GET - Unable to get data from endpoint {endpoint}")
            # elif error.response.status_code == 401:
            #     raise Http404(
            #         "401 GET - Not authorized to get data from endpoint {}".format(endpoint))
            raise error

        return response.json()

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json_data = self.get(self.url_groups, active_user)

        logger.info(
            f"GA CALL {self.url_groups.replace(GroupAdminSettings.get_group_admin_base_url(), '')}: get_groups",
            user=active_user,
        )
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_groups(self, active_user: settings.AUTH_USER_MODEL) -> GaGroupList:
        json_data = self.get_groups_raw(active_user)

        now = timezone.now()
        serializer = GaGroupListSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: GaGroupList = serializer.save()
        logger.timing(start=now, breakpoint="Serialization", function="get_groups()", user=active_user)

        return groups_response
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_group_admin_id}
    def get_group_raw(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> str:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        url = self.url_group.format(group_group_admin_id)
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_group ({url})", user=active_user)
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_group(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> GaGroup:
        if group_group_admin_id is None:
            logger.warn("GA: can't fetch a group without a group admin id", user=active_user)
            return None

        json_data = self.get_group_raw(active_user, group_group_admin_id)

        now = timezone.now()
        serializer = GaGroupSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        group: GaGroup = serializer.save()
        logger.timing(start=now, breakpoint="Serialization", function="get_group()", user=active_user)

        if group.group_admin_id != group_group_admin_id:
            logger.warn(f"GA: unknown group with group admin id {group_group_admin_id}", user=active_user)
            return None

        return group

    def get_group_serialized(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> dict:
        if group_group_admin_id is None:
            return None

        group = self.get_group(active_user=active_user, group_group_admin_id=group_group_admin_id)

        if not group:
            return None

        now = timezone.now()
        data = GaGroupSerializer(group).data
        logger.timing(start=now, breakpoint="Serialization", function="get_group_serialized()", user=active_user)

        return data

    def validate_group(self, active_user: settings.AUTH_USER_MODEL, group_group_admin_id: str) -> bool:
        serialized_group = self.get_group_serialized(active_user, group_group_admin_id)

        if serialized_group and serialized_group.get("group_admin_id") == group_group_admin_id:
            return True

        return False

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie
    def get_function_descriptions_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches a list of functions of the authenticated user for each group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        url = self.url_functions

        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_function_descriptions ({url})", user=active_user)
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_function_descriptions(self, active_user: settings.AUTH_USER_MODEL) -> GaFunctionDescriptionList:
        json_data = self.get_function_descriptions_raw(active_user)

        now = timezone.now()
        serializer = GaFunctionDescriptionListSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        function_response: GaFunctionDescriptionList = serializer.save()
        logger.timing(start=now, breakpoint="Serialization", function="get_function_descriptions()", user=active_user)

        return function_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    def get_member_profile_raw(self, active_user: settings.AUTH_USER_MODEL) -> str:
        """
        Fetches the profile information of the current user.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid
        """
        url = self.url_member_profile
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_member_profile ({url})", user=active_user)
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info_raw(self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str) -> str:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        url = self.url_member_info.format(group_admin_id)
        json_data = self.get(url, active_user)

        logger.info(f"GA CALL: get_member_info ({url})", user=active_user)
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_info(self, active_user: settings.AUTH_USER_MODEL, group_admin_id: str) -> GaProfileMember:
        json_data = self.get_member_info_raw(active_user, group_admin_id)

        now = timezone.now()
        serializer = GaMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: GaProfileMember = serializer.save()
        logger.timing(start=now, breakpoint="Serialization", function="get_member_info()", user=active_user)

        if member.group_admin_id != group_admin_id:
            logger.warn(f"GA: Unknown member with group admin id {group_admin_id}", user=active_user)
            return None

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst/filter/stateless
    def get_member_list_filtered_raw(self, active_user: settings.AUTH_USER_MODEL, payload: dict, next_url: str = None) -> str:
        url = next_url if next_url else self.url_member_list_filtered
        json_data = self.post(url, payload, active_user)

        logger.info(f"GA CALL: get_member_list_filtered ({url})", user=active_user)
        # logger.trace("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list_filtered(
        self,
        active_user: settings.AUTH_USER_MODEL,
        term: str = None,
        group_group_admin_id: str = None,
        min_age: int = None,
        max_age: int = None,
        gender: str = None,
        next_url: str = None,
        functies: list = None,
        oudleden: bool = False,
    ) -> GaListMemberPage:
        payload = {
            "criteria": {},
            "kolommen": [
                GA_COL_FIRST_NAME, GA_COL_LAST_NAME, GA_COL_BIRTH_DATE, GA_COL_GENDER,
                GA_COL_EMAIL, GA_COL_PHONE, GA_COL_FUNCTIONS,
                GA_COL_STREET_NAME, GA_COL_STREET_NUMBER, GA_COL_BUS, GA_COL_POSTAL_CODE, GA_COL_CITY,
            ],
        }
        if term:
            payload["criteria"]["naamlike"] = term
        if group_group_admin_id:
            group_number = next(
                (g.number for g in active_user.get_scouts_groups() if g.group_admin_id == group_group_admin_id),
                None,
            )
            if not group_number:
                raise ValueError(f"GA: could not find groepsnummer for group with id {group_group_admin_id}")
            payload["criteria"]["groepen"] = [group_number]
        if max_age or min_age:
            payload["criteria"]["leeftijd"] = dict()
        if max_age:
            payload["criteria"]["leeftijd"]["jongerdan"] = max_age
        if min_age:
            payload["criteria"]["leeftijd"]["ouderdan"] = min_age
        if gender:
            payload["criteria"]["geslacht"] = gender.lower()
        if functies:
            payload["criteria"]["functies"] = functies
        if oudleden:
            # True = enkel oudleden; None = ook oudleden (actief + inactief)
            payload["criteria"]["oudleden"] = True
        json_data = self.get_member_list_filtered_raw(active_user, payload, next_url)

        now = timezone.now()
        serializer = GaListMemberPageSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: GaListMemberPage = serializer.save()
        # GA does not return the member status: it follows from the request (oudleden or not)
        for member in member_list.members:
            member.active_member = not oudleden
        logger.timing(start=now, breakpoint="Serialization", function="get_member_list_filtered()", user=active_user)

        return member_list

