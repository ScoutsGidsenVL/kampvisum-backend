from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsRole
from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionSerializer(serializers.ModelSerializer):
    # scouts_group = ScoutsGroupSerializer(many=True)

    class Meta:
        model = ScoutsRole
        fields = "__all__"
