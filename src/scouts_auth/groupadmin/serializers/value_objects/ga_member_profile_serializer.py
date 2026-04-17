from scouts_auth.groupadmin.models import GaProfileMember
from scouts_auth.groupadmin.serializers.value_objects import (
    GaGroupSpecificFieldSerializer,
    GaMemberSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaMemberProfileSerializer(GaMemberSerializer):
    class Meta:
        model = GaProfileMember
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = super().to_internal_value(data)

        validated_data["group_specific_fields"] = GaGroupSpecificFieldSerializer().to_internal_value(
            data.pop("groepseigenVelden", None)
        )

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaProfileMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaProfileMember:
        if validated_data is None:
            return None

        instance = GaProfileMember()

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
