from scouts_auth.groupadmin.models import GaAddress

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaAddressSerializer(NonModelSerializer):
    class Meta:
        model = GaAddress
        abstract = True

    def to_internal_value(self, data) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in ("id", "land", "telefoon", "postadres", "status", "positie", "giscode", "omschrijving"):
            data.pop(key, None)

        validated_data = {
            "street": data.pop("straat", None),
            "number": data.pop("nummer", None),
            "letter_box": data.pop("bus", None),
            "postal_code": data.pop("postcode", None),
            "city": data.pop("gemeente", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaAddress:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaAddress:
        if validated_data is None:
            return None

        instance = GaAddress()

        instance.street = validated_data.pop("street", None)
        instance.number = validated_data.pop("number", None)
        instance.letter_box = validated_data.pop("letter_box", None)
        instance.postal_code = validated_data.pop("postal_code", None)
        instance.city = validated_data.pop("city", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
