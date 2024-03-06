"""apps.deadlines.serializers.deadline_date_serializer."""
from rest_framework import serializers

from apps.deadlines.models import DeadlineDate


class DeadlineDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadlineDate
        # fields = "__all__"
        exclude = ["deadline", "calculated_date"]
