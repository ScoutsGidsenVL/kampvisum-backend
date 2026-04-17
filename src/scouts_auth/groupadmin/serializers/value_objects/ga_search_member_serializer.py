from scouts_auth.groupadmin.models import (
    GaSearchMember,
    GaSearchMemberPage,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaPageSerializer,
)

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaSearchMemberSerializer(NonModelSerializer):
    class Meta:
        model = GaSearchMember
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "first_name": data.pop("voornaam", None),
            "last_name": data.pop("achternaam", None),
            "birth_date": data.pop("geboortedatum", None),
            "email": data.pop("email", None),
            "phone_number": data.pop("gsm", None),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", None)),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaSearchMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaSearchMember:
        if validated_data is None:
            return None

        instance = GaSearchMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.first_name = validated_data.pop("first_name", None)
        instance.last_name = validated_data.pop("last_name", None)
        instance.birth_date = validated_data.pop("birth_date", None)
        instance.email = validated_data.pop("email", None)
        instance.phone_number = validated_data.pop("phone_number", None)
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaSearchMemberPageSerializer(GaPageSerializer):
    class Meta:
        model = GaSearchMemberPage
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data = {
            "members": GaSearchMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaSearchMemberPage:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaSearchMemberPage:
        if validated_data is None:
            return None

        instance = GaSearchMemberPage()
        instance = super().update(instance, validated_data)

        instance.members = GaSearchMemberSerializer(many=True).create(
            validated_data.pop("members", [])
        )

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
