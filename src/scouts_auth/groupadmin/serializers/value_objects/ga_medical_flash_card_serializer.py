from scouts_auth.groupadmin.models import GaMedicalFlashCard
from scouts_auth.inuits.serializers import NonModelSerializer


class GaMedicalFlashCardSerializer(NonModelSerializer):
    class Meta:
        model = GaMedicalFlashCard
        abstract = True
