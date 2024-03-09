from rest_framework import serializers
from scouts_auth.inuits.serializers.fields import OptionalCharSerializerField, RequiredIntegerSerializerField

from apps.camps.serializers import CampTypeSerializer
from apps.visums.models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128)
    index = RequiredIntegerSerializerField()
    description = OptionalCharSerializerField()
    # camp_types = CampTypeSerializer(many=True)

    class Meta:
        model = Category
        # fields = "__all__"
        exclude = ["camp_types"]
