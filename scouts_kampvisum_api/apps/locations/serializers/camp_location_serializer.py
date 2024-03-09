import logging

from rest_framework import serializers
from scouts_auth.inuits.logging import InuitsLogger

from apps.locations.models import CampLocation

logger: InuitsLogger = logging.getLogger(__name__)


class CampLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampLocation
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        pk = data.get("id", None)
        data = super().to_internal_value(data)
        data["id"] = pk

        logger.debug(f"CAMP LOCATION SERIALIZER TO_INTERNAL_VALUE: {data}")

        return data
