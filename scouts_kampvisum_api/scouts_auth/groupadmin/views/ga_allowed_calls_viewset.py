"""apps.scouts_auth.groupadmin.views.ga_allowed_calls_viewset."""

import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from scouts_auth.groupadmin.models import ScoutsAllowedCalls
from scouts_auth.groupadmin.serializers import ScoutsAllowedCallsSerializer
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsAllowedCallsView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsAllowedCallsSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def view_allowed_calls(self, request):
        logger.debug("GA: Received request to view authorized groups")

        response: ScoutsAllowedCalls = self.service.get_allowed_calls(request.user)

        serializer = ScoutsAllowedCallsSerializer(response)

        return Response(serializer.data)
