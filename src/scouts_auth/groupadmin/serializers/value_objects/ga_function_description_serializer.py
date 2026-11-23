from scouts_auth.groupadmin.models import GaFunctionDescription
from scouts_auth.groupadmin.serializers.value_objects import GaGroupingSerializer

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaFunctionDescriptionSerializer(NonModelSerializer):
    class Meta:
        model = GaFunctionDescription
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in (
            "type",
            "groep",
            "groepen",
            "begin",
            "einde",
            "uiterstegeboortedatum",
            "code",
            "omschrijving",
            "beschrijving",
            "adjunct",
            "links",
        ):
            data.pop(key, None)

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "groupings": GaGroupingSerializer(many=True).to_internal_value(data.pop("groeperingen", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))
            for key in remaining_keys:
                logger.trace("UNPARSED DATA: %s", data[key])

        return validated_data

    def save(self) -> GaFunctionDescription:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaFunctionDescription:
        if validated_data is None:
            return None

        instance = GaFunctionDescription()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.groupings = GaGroupingSerializer(many=True).create(validated_data.pop("groupings", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
