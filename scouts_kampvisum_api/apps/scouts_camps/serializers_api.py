import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from .models import ScoutsCamp
from apps.scouts_groups.api.models import ScoutsSection
from apps.scouts_groups.api.serializers import (
    ScoutsSectionAPISerializer
)
from inuits.serializers import OptionalDateField


logger = logging.getLogger(__name__)


class ScoutsCampAPISerializer(serializers.ModelSerializer):
    """
    Deserializes a JSON ScoutsCamp from the frontend (no serialization).
    """
    
    name = serializers.CharField()
    start_date = OptionalDateField()
    end_date = OptionalDateField() 
    # List of ScoutsSection uuid's
    sections = ScoutsSectionAPISerializer()

    class Meta:
        model = ScoutsCamp
        fields = '__all__'
    
    def validate(self, data):
        logger.debug('SCOUTSCAMP API DATA: %s', data)

        if not data.get('name'):
            raise ValidationError(
                "A ScoutsCamp must have a name")
        
        if not data.get('sections'):
            raise ValidationError(
                "A ScoutsCamp must have at least 1 ScoutsSection attached"
            )
        else:
            for section_uuid in data.get('sections'):
                try:
                    ScoutsSection.objects.get(uuid=section_uuid)
                except ObjectDoesNotExist:
                    raise ValidationError(
                        "Invalid UUID. No ScoutsSection with that UUID: " +
                        str(section_uuid)
                    )
        
        # if data.get('start_date') and data.get('start_date') < timezone.now():
        #     raise ValidationError("The camp start date can't be in the past")

        return data

