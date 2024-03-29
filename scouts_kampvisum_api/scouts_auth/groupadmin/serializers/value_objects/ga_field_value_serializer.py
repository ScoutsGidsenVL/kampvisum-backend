from scouts_auth.groupadmin.models import AbstractScoutsValue

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AbstractScoutsValueSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsValue
        abstract = True

    def to_internal_value(self, data: tuple) -> dict:
        if data is None:
            return {}

        if data and len(data) == 2:
            (key, value) = data
            validated_data = {"key": key, "value": value}
        else:
            validated_data = {}

        return validated_data

    def save(self) -> AbstractScoutsValue:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> AbstractScoutsValue:
        if validated_data is None:
            return None

        instance = AbstractScoutsValue()

        instance.key = validated_data.pop("key", None)
        instance.value = validated_data.pop("value", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
