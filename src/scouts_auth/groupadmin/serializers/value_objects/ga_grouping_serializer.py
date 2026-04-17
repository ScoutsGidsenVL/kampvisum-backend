from scouts_auth.groupadmin.models import GaGrouping

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaGroupingSerializer(NonModelSerializer):
    class Meta:
        model = GaGrouping
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "name": data.pop("naam", None),
            "index": data.pop("volgorde", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaGrouping:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaGrouping:
        if validated_data is None:
            return None

        instance = GaGrouping()

        instance.name = validated_data.pop("name", None)
        instance.index = validated_data.pop("index", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
