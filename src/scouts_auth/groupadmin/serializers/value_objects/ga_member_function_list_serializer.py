from scouts_auth.groupadmin.models import GaMemberFunctionList
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaMemberFunctionSerializer,
    GaPageSerializer,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaMemberFunctionListSerializer(GaPageSerializer):
    class Meta:
        model = GaMemberFunctionList
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "functions": GaMemberFunctionSerializer(many=True).to_internal_value(data.pop("functies", [])),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaMemberFunctionList:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaMemberFunctionList:
        if validated_data is None:
            return None

        instance = GaMemberFunctionList()

        instance.functions = GaMemberFunctionSerializer(many=True).create(validated_data.pop("functions", []))
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
