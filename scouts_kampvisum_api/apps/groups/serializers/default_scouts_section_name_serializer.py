# LOGGING
import logging

from rest_framework import serializers

from apps.groups.models import DefaultScoutsSectionName
from apps.groups.serializers import ScoutsGroupTypeSerializer
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DefaultScoutsSectionNameSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutDefaultSectionName object
    """

    group_type = ScoutsGroupTypeSerializer()

    class Meta:
        model = DefaultScoutsSectionName
        fields = "__all__"
