# LOGGING
import logging

from rest_framework import serializers

from scouts_auth.groupadmin.models import ScoutsFunction
from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsFunctionSerializer(serializers.ModelSerializer):

    # scouts_group = ScoutsGroupSerializer(many=True)

    class Meta:
        model = ScoutsFunction
        fields = "__all__"
