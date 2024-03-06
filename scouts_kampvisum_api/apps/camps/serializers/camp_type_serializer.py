"""apps.camps.serializers.camp_type_serializer."""
# LOGGING
import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.camps.models import CampType
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampType
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        # logger.trace("CAMP TYPE SERIALIZER TO INTERNAL VALUE: %s", data)

        data = super().to_internal_value(data)
        # logger.trace("CAMP TYPE SERIALIZER TO INTERNAL VALUE: %s", data)

        return data

    def validate(self, data) -> CampType:
        if isinstance(data, CampType):
            return data

        # logger.trace("CAMP TYPE SERIALIZER VALIDATE: %s", data)
        # Safe to raise an error, because this serializer will not be used to create a CampType
        return CampType.objects.safe_get(
            id=data.get("id", None),
            camp_type=data.get("camp_type", None),
            raise_error=True,
        )
