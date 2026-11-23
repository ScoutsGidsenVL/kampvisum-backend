from scouts_auth.groupadmin.models import GaFunctionDescriptionList
from scouts_auth.groupadmin.serializers.value_objects import (
    GaFunctionDescriptionSerializer,
    GaPageSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaFunctionDescriptionListSerializer(GaPageSerializer):
    class Meta:
        model = GaFunctionDescriptionList
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # GA returns links, the app doesn't use them
        data.pop("links", None)

        validated_data = {
            "function_descriptions": GaFunctionDescriptionSerializer(many=True).to_internal_value(
                data.pop("functies", [])
            ),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaFunctionDescriptionList:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaFunctionDescriptionList:
        if validated_data is None:
            return None

        instance = GaFunctionDescriptionList()

        instance.function_descriptions = GaFunctionDescriptionSerializer(many=True).create(
            validated_data.pop("function_descriptions", [])
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
