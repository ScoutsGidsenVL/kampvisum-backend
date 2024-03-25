"""apps.scouts_auth.groupadmin.serializers.value_objects.ga_member_medical_flash_card_serializer."""

from scouts_auth.groupadmin.models import AbstractScoutsMedicalFlashCard
from scouts_auth.inuits.serializers import NonModelSerializer


class AbstractScoutsMedicalFlashCardSerializer(NonModelSerializer):
    class Meta:
        model = AbstractScoutsMedicalFlashCard
        abstract = True
