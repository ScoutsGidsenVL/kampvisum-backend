import datetime

from scouts_auth.groupadmin.models import (
    GaMemberPersonalData,
    GaMemberGroupAdminData,
    GaMemberScoutsData,
    GaProfileMember,
    GaAddress,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaContactSerializer,
    GaAddressSerializer,
    GaMemberFunctionSerializer,
    GaGroupSerializer,
    GaGroupSpecificFieldSerializer,
)

from scouts_auth.inuits.models import GenderHelper
from scouts_auth.inuits.serializers import NonModelSerializer

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaMemberPersonalDataSerializer(NonModelSerializer):
    class Meta:
        model = GaMemberPersonalData
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data: dict = {
            "gender": data.pop("geslacht", None),
            "phone_number": data.pop("gsm", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaMemberPersonalData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaMemberPersonalData:
        if validated_data is None:
            return None

        instance = GaMemberPersonalData()

        instance.gender = GenderHelper.parse_gender(validated_data.pop("gender", None))
        instance.phone_number = validated_data.pop("phone_number", None)

        if instance.phone_number:
            instance.phone_number = "".join(instance.phone_number.split())

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaMemberGroupAdminDataSerializer(NonModelSerializer):
    class Meta:
        model = GaMemberGroupAdminData
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data: dict = {
            "first_name": data.pop("voornaam", None),
            "last_name": data.pop("achternaam", None),
            "birth_date": data.pop("geboortedatum", None),
        }

        if validated_data.get("birth_date", None):
            validated_data["birth_date"] = datetime.datetime.strptime(
                validated_data.get("birth_date")[:10], "%Y-%m-%d"
            ).date()

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaMemberGroupAdminData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaMemberGroupAdminData:
        if validated_data is None:
            return None

        instance = GaMemberGroupAdminData()

        instance.first_name = validated_data.pop("first_name", None)
        instance.last_name = validated_data.pop("last_name", None)
        instance.birth_date = validated_data.pop("birth_date", None)

        if isinstance(instance.birth_date, str):
            instance.birth_date = datetime.datetime.strptime(instance.birth_date, "%Y-%m-%d").date()

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaMemberScoutsDataSerializer(NonModelSerializer):
    class Meta:
        model = GaMemberScoutsData
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data: dict = {
            "membership_number": data.pop("lidnummer", None),
            "customer_number": data.pop("klantnummer", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaMemberScoutsData:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaMemberScoutsData:
        if validated_data is None:
            return None

        instance = GaMemberScoutsData()

        instance.membership_number = validated_data.pop("membership_number", None)
        instance.customer_number = validated_data.pop("customer_number", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaMemberSerializer(NonModelSerializer):
    class Meta:
        model = GaProfileMember
        abstract = True

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return {}

        validated_data: dict = {
            "personal_data": GaMemberPersonalDataSerializer().to_internal_value(
                data.pop("persoonsgegevens", None)
            ),
            "group_admin_data": GaMemberGroupAdminDataSerializer().to_internal_value(
                data.pop("vgagegevens", None)
            ),
            "scouts_data": GaMemberScoutsDataSerializer().to_internal_value(
                data.pop("verbondsgegevens", None)
            ),
            "email": data.pop("email", None),
            "username": data.pop("gebruikersnaam", None),
            "group_admin_id": data.pop("id", None),
            "inactive_member": False,
            "addresses": GaAddressSerializer(many=True).to_internal_value(data.pop("adressen", [])),
            "contacts": GaContactSerializer(many=True).to_internal_value(data.pop("contacten", [])),
            "functions": GaMemberFunctionSerializer(many=True).to_internal_value(data.pop("functies", [])),
            "scouts_groups": GaGroupSerializer(many=True).to_internal_value(data.pop("groepen", [])),
            "group_specific_fields": GaGroupSpecificFieldSerializer().to_internal_value(
                data.pop("groepseigenVelden", {})
            ),
            "links": GaLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GaProfileMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GaProfileMember:
        if validated_data is None:
            return None

        instance = GaProfileMember()

        instance.personal_data = GaMemberPersonalDataSerializer().create(
            validated_data.pop("personal_data", None)
        )
        instance.group_admin_data = GaMemberGroupAdminDataSerializer().create(
            validated_data.pop("group_admin_data", None)
        )
        instance.scouts_data = GaMemberScoutsDataSerializer().create(
            validated_data.pop("scouts_data", None)
        )
        instance.email = validated_data.pop("email", None)
        instance.username = validated_data.pop("username", None)
        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.inactive_member = False
        instance.addresses = GaAddressSerializer(many=True).create(validated_data.pop("addresses", []))
        instance.contacts = GaContactSerializer(many=True).create(validated_data.pop("contacts", []))
        instance.functions = GaMemberFunctionSerializer(many=True).create(validated_data.pop("functions", []))
        instance.scouts_groups = GaGroupSerializer(many=True).create(
            validated_data.pop("scouts_groups", [])
        )
        instance.group_specific_fields = GaGroupSpecificFieldSerializer().create(
            validated_data.pop("group_specific_fields", {})
        )
        instance.links = GaLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.api("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GaSearchMemberFrontendSerializer(NonModelSerializer):
    class Meta:
        model = GaProfileMember
        abstract = True

    def to_representation(self, instance: GaProfileMember) -> dict:
        serialized = {}

        serialized["group_admin_id"] = instance.group_admin_id
        serialized["gender"] = instance.personal_data.gender
        serialized["email"] = instance.email
        serialized["phone_number"] = instance.personal_data.phone_number
        serialized["first_name"] = instance.group_admin_data.first_name
        serialized["last_name"] = instance.group_admin_data.last_name
        serialized["birth_date"] = instance.group_admin_data.birth_date
        serialized["membership_number"] = instance.scouts_data.membership_number
        serialized["customer_number"] = instance.scouts_data.customer_number
        serialized["inactive_member"] = instance.inactive_member

        if instance.addresses and len(instance.addresses) > 0:
            address: GaAddress = instance.addresses[0]
            serialized["street"] = address.street
            serialized["number"] = address.number
            serialized["letter_box"] = address.letter_box
            serialized["postal_code"] = address.postal_code
            serialized["city"] = address.city
        else:
            serialized["street"] = None
            serialized["number"] = None
            serialized["letter_box"] = None
            serialized["postal_code"] = None
            serialized["city"] = None

        return serialized


class GaMemberFrontendSerializer(NonModelSerializer):
    class Meta:
        model = GaProfileMember
        abstract = True

    def to_representation(self, instance: GaProfileMember) -> dict:
        serialized: dict = super().to_representation(instance)

        serialized["group_admin_id"] = instance.group_admin_id
        serialized["gender"] = instance.personal_data.gender
        serialized["email"] = instance.email
        serialized["phone_number"] = instance.personal_data.phone_number
        serialized["first_name"] = instance.group_admin_data.first_name
        serialized["last_name"] = instance.group_admin_data.last_name
        serialized["birth_date"] = instance.group_admin_data.birth_date
        serialized["membership_number"] = instance.scouts_data.membership_number
        serialized["customer_number"] = instance.scouts_data.customer_number
        serialized["inactive_member"] = instance.inactive_member

        if instance.addresses and len(instance.addresses) > 0:
            address: GaAddress = instance.addresses[0]
            serialized["street"] = address.street
            serialized["number"] = address.number
            serialized["letter_box"] = address.letter_box
            serialized["postal_code"] = address.postal_code
            serialized["city"] = address.city
        else:
            serialized["street"] = None
            serialized["number"] = None
            serialized["letter_box"] = None
            serialized["postal_code"] = None
            serialized["city"] = None

        return serialized
