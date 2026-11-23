from scouts_auth.groupadmin.models import (
    GaListMember,
    GaListMemberPage,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    GaValueSerializer,
    GaPageSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaListMemberSerializer(NonModelSerializer):
    class Meta:
        model = GaListMember
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in ("positie", "links"):
            data.pop(key, None)

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "values": GaValueSerializer(many=True).to_internal_value(list(data.pop("waarden", {}).items())),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> GaListMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaListMember:
        if validated_data is None:
            return None

        # active_member stays unset: GA does not return it, the caller sets it
        instance = GaListMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.values = GaValueSerializer(many=True).create(validated_data.pop("values", {}))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaListMemberPageSerializer(GaPageSerializer):
    class Meta:
        model = GaListMemberPage
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "members": GaListMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> GaListMemberPage:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaListMemberPage:
        if validated_data is None:
            return None

        instance = GaListMemberPage()
        instance.members = GaListMemberSerializer(many=True).create(validated_data.pop("members", []))
        instance = super().update(instance, validated_data)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
