from django.db import models
from django.utils import timezone
from rest_framework import serializers

from apps.base.models import RecursiveField
from ..models import ScoutsGroup
from ..serializers import ScoutsGroupTypeSerializer


class ScoutsGroupSerializer(serializers.ModelSerializer):
    """
    Serializes a ScoutGroup object.
    """
    
    group_admin_id = serializers.CharField(default='')
    number = serializers.CharField(default='')
    name = serializers.CharField(default='')
    foundation = serializers.DateTimeField(default=timezone.now)
    only_leaders = serializers.BooleanField(default=False)
    show_members_improved = serializers.BooleanField(default=False)
    email = serializers.CharField(default='')
    website = serializers.CharField(default='')
    info = serializers.CharField(default='')
    sub_groups = RecursiveField(default=list(), many=True)
    type = ScoutsGroupTypeSerializer()
    public_registration = serializers.BooleanField(default=False)
    
    class Meta:
        model = ScoutsGroup
        fields = '__all__'
    
    def create(self, validated_data) -> ScoutsGroup:
        return ScoutsGroup(**validated_data)
    
    def update(self, instance: ScoutsGroup, validated_data) -> ScoutsGroup:
        instance.group_admin_id = validated_data.get(
            'group_admin_id', instance.group_admin_id)
        instance.number = validated_data.get(
            'number', instance.number)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.foundation = validated_data.get(
            'foundation', instance.foundation)
        instance.only_leaders = validated_data.get(
            'only_leaders', instance.only_leaders)
        instance.show_members_improved = validated_data.get(
            'show_members_improved', instance.show_members_improved)
        instance.email = validated_data.get('email', instance.email)
        instance.website = validated_data.get('website', instance.website)
        instance.info = validated_data.get('info', instance.info)
        instance.sub_groups = ScoutsGroupSerializer(many=True)
        instance.type = ScoutsGroupTypeSerializer()
        instance.public_registration = validated_data.get(
            'public_registration', instance.public_registration)
        
        return instance
