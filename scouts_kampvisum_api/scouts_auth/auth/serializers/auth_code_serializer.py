"""scouts_auth.auth.serializers.auth_code_serializer."""

from rest_framework import serializers


class AuthCodeSerializer(serializers.Serializer):
    authCode = serializers.CharField()
    redirectUri = serializers.CharField()
