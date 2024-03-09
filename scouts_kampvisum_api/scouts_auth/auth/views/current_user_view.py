import logging
from typing import List

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, views
from rest_framework.response import Response

from scouts_auth.auth.models import User
from scouts_auth.auth.serializers import UserSerializer
from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.groupadmin.serializers import ScoutsUserSerializer
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer})
    def get(self, request):
        logger.debug("/me", user=request.user)

        serializer = ScoutsUserSerializer(request.user)
        data = serializer.data

        return Response(data)
