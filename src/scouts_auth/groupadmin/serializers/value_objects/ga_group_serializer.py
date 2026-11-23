from scouts_auth.groupadmin.models import GaGroup

from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaGroupSerializer(NonModelSerializer):
    """Serializes a Group instance to a string."""

    class Meta:
        model = GaGroup
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        # Keys GA returns, but the app doesn't use
        for key in (
            "opgericht",
            "rekeningnummer",
            "email",
            "website",
            "vrijeInfo",
            "bovenliggendeGroep",
            "enkelLeiding",
            "ledenVerbeterdTonen",
            "adressen",
            "contacten",
            "groepseigenVelden",
            "groepseigenGegevens",
            "groepseigenFuncties",
            "facturatieLeden",
            "facturatieLeiding",
            "evenementSchrijfRecht",
            "verantwoordelijkheden",
            "publiek-inschrijven",
            "instantie",
            "links",
        ):
            data.pop(key, None)

        validated_data: dict = {
            "group_admin_id": data.pop("id", None),
            "number": data.pop("groepsnummer", None),
            "name": data.pop("naam", None),
            "child_groups": data.pop("onderliggendeGroepen", []),
            "type": data.pop("soort", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaGroup:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GaGroup:
        if validated_data is None:
            return None

        instance = GaGroup()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.number = validated_data.pop("number", None)
        instance.name = validated_data.pop("name", None)
        instance.child_groups = validated_data.pop("child_groups", None)
        instance.type = validated_data.pop("type", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
