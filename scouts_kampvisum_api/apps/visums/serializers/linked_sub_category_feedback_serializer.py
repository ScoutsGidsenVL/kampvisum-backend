# LOGGING
import logging

from rest_framework import serializers

from apps.visums.models import LinkedSubCategory
from apps.visums.models.enums import CheckState
from apps.visums.serializers import (LinkedCheckSerializer,
                                     SubCategorySerializer)
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.serializers import PermissionRequiredSerializerField
from scouts_auth.inuits.serializers.fields import (DefaultCharSerializerField,
                                                   OptionalCharSerializerField)

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedSubCategoryFeedbackSerializer(serializers.ModelSerializer):

    feedback = PermissionRequiredSerializerField(
        permission="visums.change_campvisum_feedback",
        field=OptionalCharSerializerField(),
        required=True,
    )

    class Meta:
        model = LinkedSubCategory
        fields = ["feedback"]
