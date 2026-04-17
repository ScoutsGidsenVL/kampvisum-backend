from scouts_auth.groupadmin.models import GaMemberFunction
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaGroupSerializer,
)

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

        validated_data = {
            "scouts_group": GaGroupSerializer().to_internal_value({"id": data.pop("groep", None)}),
            "function": data.pop("functie", None),
            "begin": DateUtils.datetime_from_isoformat(data.pop("begin", None)),
            "end": DateUtils.datetime_from_isoformat(data.pop("einde", None)),
            "code": data.pop("code", None),
            "description": data.pop("omschrijving", data.pop("beschrijving", None)),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
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
        instance.begin = validated_data.pop("begin", None)
        instance.end = validated_data.pop("end", None)
        instance.code = validated_data.pop("code", None)
        instance.description = validated_data.pop("description", None)
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
