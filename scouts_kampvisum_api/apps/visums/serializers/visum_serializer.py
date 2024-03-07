# LOGGING
import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.camps.serializers import CampTypeSerializer, CampYearSerializer
from apps.camps.services import CampYearService
from apps.groups.models import ScoutsSection
from apps.groups.serializers import ScoutsSectionSerializer
from apps.visums.models import CampVisum
from apps.visums.serializers import (
    CampVisumEngagementSerializer,
    CampVisumEngagementSimpleSerializer,
    LinkedCategorySetSerializer,
)
from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import OptionalCharSerializerField

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumSerializer(serializers.ModelSerializer):
    group = ScoutsGroupSerializer(required=False)
    year = CampYearSerializer()
    sections = ScoutsSectionSerializer(many=True)
    camp_types = CampTypeSerializer(many=True)
    category_set = LinkedCategorySetSerializer()
    engagement = CampVisumEngagementSerializer(required=False)
    notes = PermissionRequiredSerializerField(
        permission="visums.view_campvisum_notes",
        field=OptionalCharSerializerField(),
        required=False,
    )

    class Meta:
        model = CampVisum
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        pk = data.get("id")
        instance: CampVisum = CampVisum.objects.safe_get(id=pk)
        if instance:
            return instance

        data["category_set"] = {}
        data["engagement"] = {}
        data["year"] = data.get("year", None)
        if not data["year"]:
            year = CampYearService().get_or_create_current_camp_year()
            data["year"] = year.year

        group = data.get("group", None)
        if not group:
            sections = data.get("sections", [])
            if sections and len(sections) > 0:
                section = ScoutsSection.objects.safe_get(
                    id=sections[0], user=self.context["request"].user, raise_error=True
                )
                group = section.group
        if not group:
            raise ValidationError(
                f"[{self.context['request'].user.username}] Scouts group's group admin id must be provided"
            )
        group = self.context["request"].user.get_scouts_group(group_admin_id=group, raise_error=True)
        data["group"] = group
        data["group_name"] = group.name

        data = super().to_internal_value(data)
        logger.debug("DATA: %s", data)

        return data

    def to_representation(self, obj: CampVisum) -> dict:
        data = super().to_representation(obj)

        data["group_group_admin_id"] = data.get("group", {}).get("group_admin_id", None)

        return data


class CampVisumOverviewSerializer(serializers.Serializer):
    def to_representation(self, data: dict) -> dict:
        # data["group"] = self.context['request'].user.get_scouts_group(
        #     data["group"])
        data["group_group_admin_id"] = data["group"]
        if self.context["list_dc_overview"]:
            camp = CampVisum.objects.get(id=data["id"])
            if camp.state != "DATA_REQUIRED":
                if camp.camp_registration_mail_sent_before_deadline:
                    data["registration_status"] = "on_time"
                else:
                    data["registration_status"] = "late"
            else:
                data["registration_status"] = "not_complete"
            data["engagement"] = CampVisumEngagementSimpleSerializer(camp.engagement).data
        return data
