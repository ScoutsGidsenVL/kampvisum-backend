from scouts_auth.groupadmin.models import (
    GaListMember,
    GaListMemberPage,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    GaValueSerializer,
    GaLinkSerializer,
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

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "index": data.pop("positie", None),
            "values": GaValueSerializer(many=True).to_internal_value(list(data.pop("waarden", {}).items())),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
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

        instance = GaListMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.index = validated_data.pop("index", None)
        instance.values = GaValueSerializer(many=True).create(validated_data.pop("values", {}))
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

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

        super().create(validated_data)

        logger.debug("INSTANCE: %s", instance)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
