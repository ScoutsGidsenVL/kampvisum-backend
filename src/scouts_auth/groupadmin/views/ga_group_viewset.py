from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from scouts_auth.groupadmin.models import (
    GaGroup,
    GaGroupList,
)
from scouts_auth.groupadmin.serializers import (
    GaGroupSerializer,
    GaGroupListSerializer,
)
from scouts_auth.groupadmin.services import GroupAdmin


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class GaGroupView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: GaGroupSerializer})
    @action(methods=["GET"], url_path="", detail=False)
    def view_groups(self, request):
        logger.debug("GA: Received request to view authorized groups")

        response_groups: GaGroupList = self.service.get_groups(request.user)
        groups = response_groups.scouts_groups

        serializer = GaGroupSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GaGroupListSerializer})
    @action(methods=["GET"], url_path="", detail=False)
    def view_accountable_groups(self, request):
        logger.debug("GA: Received request for groups for which the authorized user is accountable (/vga call)")

        response_groups: GaGroupList = self.service.get_accountable_groups(request.user)
        groups = response_groups.scouts_groups

        serializer = GaGroupListSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GaGroupSerializer})
    @action(methods=["GET"], url_path=r"(?P<group_group_admin_id>\w+)", detail=False)
    def view_group(self, request, group_group_admin_id: str):
        logger.debug(
            "GA: Received request for group info (group_group_admin_id: %s)",
            group_group_admin_id,
        )

        group: GaGroup = self.service.get_group(request.user, group_group_admin_id)

        serializer = GaGroupSerializer(group)

        return Response(serializer.data)
