from apps.deadlines.models import LinkedDeadlineFlag
from apps.deadlines.serializers import DeadlineFlagSerializer
from rest_framework import serializers


class LinkedDeadlineFlagSerializer(serializers.ModelSerializer):

    parent = DeadlineFlagSerializer()

    class Meta:
        model = LinkedDeadlineFlag
        fields = "__all__"
