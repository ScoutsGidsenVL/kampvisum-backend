from scouts_auth.groupadmin.models import GaLink

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaLinkSerializer(NonModelSerializer):
    class Meta:
        model = GaLink
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in ("method", "secties"):
            data.pop(key, None)

        validated_data = {
            "rel": data.pop("rel", None),
            "href": data.pop("href", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaLink:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaLink:
        if validated_data is None:
            return None

        instance = GaLink()

        instance.rel = validated_data.pop("rel", None)
        instance.href = validated_data.pop("href", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
