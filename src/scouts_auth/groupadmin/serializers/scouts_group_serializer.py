from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsGroup


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutsGroup
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:
        if isinstance(data, ScoutsGroup):
            return data

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: ScoutsGroup) -> dict:
        if not isinstance(obj, ScoutsGroup):
            obj = self.context["request"].user.get_scouts_group(obj, raise_error=True)

        if not obj:
            return {}

        return {
            # The frontend expects the groepsnummer under this key
            "group_admin_id": obj.number,
            "number": obj.number,
            "name": obj.name,
            "full_name": obj.full_name,
            "type": obj.type,
        }

    def validate(self, data: dict) -> ScoutsGroup:
        if isinstance(data, ScoutsGroup):
            return data

        logger.debug("SCOUTS GROUP SERIALIZER VALIDATE: %s", data)
        group = ScoutsGroup.objects.safe_get(number=data.get("number"))

        if group:
            return group

        return ScoutsGroup(**data)
