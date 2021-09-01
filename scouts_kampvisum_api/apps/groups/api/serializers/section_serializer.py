import logging
from rest_framework import serializers

from ..models import Section
from ..serializers import (
    GroupSerializer,
    SectionNameSerializer,
    SectionNameAPISerializer,
)
from inuits.mixins import FlattenMixin


logger = logging.getLogger(__name__)


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutSection object
    """

    group = GroupSerializer()
    name = SectionNameSerializer()
    hidden = serializers.BooleanField()

    class Meta:
        model = Section
        fields = "__all__"


class SectionAPISerializer(FlattenMixin, serializers.ModelSerializer):
    """
    Serializes a ScoutsSection object for use in camp visum views.
    """

    class Meta:
        model = Section
        fields = ["uuid"]
        flatten = [("name", SectionNameAPISerializer)]


class SectionCreationAPISerializer(serializers.Serializer):
    """
    Deserializes ScoutSection JSON data into a SectionObject.
    """

    name = serializers.JSONField()

    def validate(self, data):
        if data["name"] is None:
            raise serializers.ValidationError("Section name can't be null")

        return data
