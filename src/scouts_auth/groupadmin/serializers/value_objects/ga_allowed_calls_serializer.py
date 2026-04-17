from scouts_auth.groupadmin.models import GaAllowedCalls
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaAllowedCallsSerializer(NonModelSerializer):
    class Meta:
        model = GaAllowedCalls
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {"links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", []))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaAllowedCalls:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaAllowedCalls:
        if validated_data is None:
            return None

        instance = GaAllowedCalls()

        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
