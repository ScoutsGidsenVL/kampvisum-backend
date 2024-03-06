"""apps.deadlines.serializers.deadline_item_serializer."""
# LOGGING
import logging

from rest_framework import serializers

from apps.deadlines.models import DeadlineItem
from apps.deadlines.serializers import DeadlineFlagSerializer
from apps.visums.serializers import CheckSerializer, SubCategorySerializer
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineItemSerializer(serializers.ModelSerializer):

    item_flag = DeadlineFlagSerializer(required=False)
    item_sub_category = SubCategorySerializer(required=False)
    item_check = CheckSerializer(required=False)

    class Meta:
        model = DeadlineItem
        fields = "__all__"
