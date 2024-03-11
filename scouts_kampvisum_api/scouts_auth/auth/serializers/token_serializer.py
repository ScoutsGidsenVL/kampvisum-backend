"""apps.scouts_auth.serializers.token_serializer."""
from rest_framework import serializers


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
