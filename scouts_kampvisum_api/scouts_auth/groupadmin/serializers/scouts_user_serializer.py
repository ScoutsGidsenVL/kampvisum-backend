from typing import List

from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsUser, ScoutsGroup, ScoutsFunction
from scouts_auth.groupadmin.settings import GroupAdminSettings

from scouts_auth.inuits.utils import ListUtils


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()
    scouts_functions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        exclude = ["password"]

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions

    def get_scouts_groups(self, obj: ScoutsUser) -> List[dict]:
        # groups = []

        # admin_groups: List[ScoutsGroup] = list(ScoutsGroup.objects.get_by_group_admin_ids(
        #     GroupAdminSettings.get_administrator_groups()))

        # for admin_group in admin_groups:
        #     if obj.has_role_leader(group=admin_group):
        #         groups = ScoutsGroup.objects.all()
        #         break

        # if not groups:
        #     groups: List[ScoutsGroup] = [
        #         group
        #         for group in obj.scouts_groups
        #         if obj.has_role_leader(group=group)
        #         or obj.has_role_district_commissioner(group=group)
        #     ]

        #     if obj.has_role_district_commissioner():
        #         district_commissioner_groups = obj.get_district_commissioner_groups()

        #         groups: List[ScoutsGroup] = ListUtils.concatenate_unique_lists(
        #             groups, district_commissioner_groups
        #         )

        #         groups.sort(key=lambda group: group.group_admin_id)

        return [
            {
                "group_admin_id": scouts_group.group_admin_id,
                "name": scouts_group.name,
                "full_name": scouts_group.full_name,
                "type": scouts_group.type,
                "is_section_leader": obj.has_role_section_leader(scouts_group=scouts_group),
                "is_group_leader": obj.has_role_group_leader(scouts_group=scouts_group),
                "is_district_commissioner": obj.has_role_district_commissioner(
                    scouts_group=scouts_group
                ),
                "is_shire_president": obj.has_role_shire_president(
                    scouts_group=scouts_group
                ),
                "is_admin": obj.has_role_administrator(),
            }
            for scouts_group in obj.scouts_groups
        ]

    def get_scouts_functions(self, obj: ScoutsUser) -> List[dict]:
        return [
            {
                "group_admin_id": scouts_function.group_admin_id,
                "scouts_group": scouts_function.scouts_group.group_admin_id,
                "code": scouts_function.code,
                "description": scouts_function.description,
                "is_leader": scouts_function.is_leader_function(),
                "is_section_leader": scouts_function.is_section_leader_function(),
                "is_group_leader": scouts_function.is_group_leader_function(),
                "is_district_commissioner": scouts_function.is_district_commissioner_function(),
                "is_shire_president": scouts_function.is_shire_president_function(),
                "end": scouts_function.end,
            }
            for scouts_function in obj.scouts_functions
        ]

    def to_internal_value(self, data: dict) -> dict:
        group_admin_id = data.get("group_admin_id", None)
        if group_admin_id:
            return ScoutsUser.objects.safe_get(
                group_admin_id=group_admin_id, raise_error=True
            )

        return super().to_internal_value(data)
