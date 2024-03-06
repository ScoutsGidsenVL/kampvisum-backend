# LOGGING
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from scouts_auth.groupadmin.models import (AbstractScoutsGroup,
                                           AbstractScoutsGroupListResponse)
from scouts_auth.groupadmin.serializers import (
    AbstractScoutsGroupListResponseSerializer, AbstractScoutsGroupSerializer)
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class AbstractScoutsGroupView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: AbstractScoutsGroupSerializer})
    @action(methods=["GET"], url_path="", detail=False)
    def view_groups(self, request):
        logger.debug("GA: Received request to view authorized groups")

        response_groups: AbstractScoutsGroupListResponse = self.service.get_groups(
            request.user
        )
        groups = response_groups.scouts_groups

        serializer = AbstractScoutsGroupSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: AbstractScoutsGroupListResponseSerializer}
    )
    @action(methods=["GET"], url_path="", detail=False)
    def view_accountable_groups(self, request):
        logger.debug(
            "GA: Received request for groups for which the authorized user is accountable (/vga call)"
        )

        response_groups: AbstractScoutsGroupListResponse = (
            self.service.get_accountable_groups(request.user)
        )
        groups = response_groups.scouts_groups

        serializer = AbstractScoutsGroupListResponseSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: AbstractScoutsGroupSerializer})
    @action(methods=["GET"], url_path=r"(?P<group_group_admin_id>\w+)", detail=False)
    def view_group(self, request, group_group_admin_id: str):
        logger.debug(
            "GA: Received request for group info (group_group_admin_id: %s)",
            group_group_admin_id,
        )

        group: AbstractScoutsGroup = self.service.get_group(
            request.user, group_group_admin_id
        )

        serializer = AbstractScoutsGroupSerializer(group)

        return Response(serializer.data)
