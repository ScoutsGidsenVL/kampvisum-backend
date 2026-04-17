from scouts_auth.groupadmin.models import GaGroupList
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaGroupSerializer,
    GaPageSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaGroupListSerializer(GaPageSerializer):
    class Meta:
        model = GaGroupList
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "scouts_groups": GaGroupSerializer(many=True).to_internal_value(data.pop("groepen", [])),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def create(self, validated_data: dict) -> GaGroupList:
        if validated_data is None:
            return None

        instance = GaGroupList()

        instance.scouts_groups = GaGroupSerializer(many=True).create(
            validated_data.pop("scouts_groups", [])
        )
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
