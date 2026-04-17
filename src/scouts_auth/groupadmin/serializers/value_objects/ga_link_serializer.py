from typing import List

from scouts_auth.groupadmin.models import GaLink

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaLinkSectionSerializer(NonModelSerializer):
    def to_internal_value(self, data: List[str]) -> list:
        if data is None:
            return []

        return data

    def save(self) -> List[str]:
        return self.create(self.validated_data)

    def create(self, validated_data: List[str]) -> List[str]:
        if validated_data is None:
            return []

        return validated_data


class GaLinkSerializer(NonModelSerializer):
    class Meta:
        model = GaLink
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "rel": data.pop("rel", None),
            "href": data.pop("href", None),
            "method": data.pop("method", None),
            "sections": GaLinkSectionSerializer().to_internal_value(data.pop("secties", None)),
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
        instance.method = validated_data.pop("method", None)
        instance.sections = GaLinkSectionSerializer().create(validated_data.pop("sections", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
