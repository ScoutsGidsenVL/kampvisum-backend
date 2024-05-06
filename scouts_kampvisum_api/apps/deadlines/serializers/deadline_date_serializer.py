from apps.deadlines.models import DeadlineDate
from rest_framework import serializers


class DeadlineDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeadlineDate
        # fields = "__all__"
        exclude = ["deadline", "calculated_date"]
