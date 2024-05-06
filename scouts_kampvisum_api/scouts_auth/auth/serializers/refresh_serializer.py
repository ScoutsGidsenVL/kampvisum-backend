"""scouts_auth.auth.serializers.refresh_serializer."""

from rest_framework import serializers


class RefreshSerializer(serializers.Serializer):
    refreshToken = serializers.CharField()
