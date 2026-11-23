from scouts_auth.groupadmin.models import GaMemberFunction
from scouts_auth.groupadmin.serializers.value_objects import GaGroupSerializer

from scouts_auth.inuits.serializers import NonModelSerializer
from scouts_auth.inuits.utils import DateUtils

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaMemberFunctionSerializer(NonModelSerializer):
    class Meta:
        model = GaMemberFunction
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in ("begin", "links"):
            data.pop(key, None)

        validated_data = {
            "scouts_group": GaGroupSerializer().to_internal_value({"id": data.pop("groep", None)}),
            "function": data.pop("functie", None),
            "end": DateUtils.datetime_from_isoformat(data.pop("einde", None)),
            "code": data.pop("code", None),
            "description": data.pop("omschrijving", data.pop("beschrijving", None)),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))
            for key in remaining_keys:
                logger.trace("UNPARSED DATA: %s", data[key])

        return validated_data

    def save(self) -> GaMemberFunction:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaMemberFunction:
        if validated_data is None:
            return None

        instance = GaMemberFunction()

        instance.scouts_group = GaGroupSerializer().create(validated_data.pop("scouts_group", None))
        instance.function = validated_data.pop("function", None)
        instance.end = validated_data.pop("end", None)
        instance.code = validated_data.pop("code", None)
        instance.description = validated_data.pop("description", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
