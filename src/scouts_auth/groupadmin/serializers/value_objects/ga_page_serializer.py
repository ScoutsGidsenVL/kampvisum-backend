from scouts_auth.groupadmin.models import GaPage
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaPageSerializer(NonModelSerializer):
    class Meta:
        model = GaPage
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Paging metadata GA returns, but the app doesn't use: paging follows the "next" link
        for key in ("aantal", "totaal", "offset", "filtercriterium", "criteria"):
            data.pop(key, None)

        validated_data = {
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaPage:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaPage:
        if validated_data is None:
            return None

        instance = GaPage()

        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        return instance

    def update(self, instance: GaPage, validated_data: dict) -> GaPage:
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        return instance
