"""apps.scouts_auth.views.logout_view."""

import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.response import Response

from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.scouts.services import ScoutsUserSessionService

logger: InuitsLogger = logging.getLogger(__name__)


class LogoutView(views.APIView):
    service = ScoutsUserSessionService()

    @swagger_auto_schema(responses={status.HTTP_200_OK})
    def get(self, request):
        logger.debug(f"LOGOUT", user=request.user)

        self.service.remove_user_from_session(request.user.username)

        return Response(f"[{request.user.username}] LOGGED OUT")
