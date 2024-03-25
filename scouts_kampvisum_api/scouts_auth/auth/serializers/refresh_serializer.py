"""apps.scouts_auth.serializers.refresh_serializer."""

from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()
