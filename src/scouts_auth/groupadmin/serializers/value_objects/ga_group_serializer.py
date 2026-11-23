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

        # Keys GA returns, but the app doesn't use.
        # "id" is an internal GA id: the app identifies groups by their groepsnummer.
        for key in (
            "id",
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
            "onderliggendeGroepen",
            "publiek-inschrijven",
            "instantie",
            "links",
        ):
            data.pop(key, None)

        validated_data: dict = {
            "number": data.pop("groepsnummer", None),
            "name": data.pop("naam", None),
            # GA sends null for a group over which the user has no responsibilities
            "responsibilities": data.pop("verantwoordelijkheden", None) or [],
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

        instance.number = validated_data.pop("number", None)
        instance.name = validated_data.pop("name", None)
        instance.responsibilities = validated_data.pop("responsibilities", None) or []
        instance.type = validated_data.pop("type", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
