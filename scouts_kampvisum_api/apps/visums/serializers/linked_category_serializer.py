from rest_framework import serializers

from apps.visums.models import LinkedCategory
from apps.visums.models.enums import CheckState
from apps.visums.serializers import CategorySerializer, LinkedSubCategorySerializer

from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import OptionalCharSerializerField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCategorySerializer(serializers.ModelSerializer):

    parent = CategorySerializer()
    sub_categories = LinkedSubCategorySerializer(many=True)
    notes = PermissionRequiredSerializerField(
        permission="visums.view_visum_notes",
        field=OptionalCharSerializerField(),
        required=False,
    )

    class Meta:
        model = LinkedCategory
        exclude = ["category_set"]

    def to_representation(self, obj: LinkedCategory) -> dict:
        if obj.is_archived:
            return None

        # logger.debug("LINKED CATEGORY TO_REPRESENTATION: %s", obj)

        data = super().to_representation(obj)

        # logger.debug("LINKED CATEGORY TO_REPRESENTATION: %s", obj)

        data["state"] = CheckState.CHECKED
        for sub_category in data.get("sub_categories", []):
            if CheckState.is_unchecked(sub_category.get("state", CheckState.UNCHECKED)):
                data["state"] = CheckState.UNCHECKED
                break

        data["readable_name"] = obj.readable_name

        data["camp"] = {}
        data["visum"] = {}

        visum = obj.category_set.visum

        data["camp"]["name"] = visum.camp.name
        data["visum"]["id"] = visum.id

        return data
