"""apps.setup.views."""
import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from scouts_auth.inuits.logging import InuitsLogger

import apps.setup.models as setup_models

logger: InuitsLogger = logging.getLogger(__name__)


class SetupViewSet(viewsets.GenericViewSet):
    """
    A viewset for handling basic application setup.
    """

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="setup",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: setup_models.SetupSerializer})
    def check(self, request):
        """
        Returns a simple JSON list that describes the initial data status.
        """

        instance = setup_models.Setup()
        serializer = setup_models.SetupSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="setup/init",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: setup_models.SetupSerializer})
    def init(self, request):
        """
        Returns a simple JSON list that describes the initial data status.
        """
        instance = setup_models.Setup()
        instance.perform_init(request)
        serializer = setup_models.SetupSerializer(instance, context={"request": request})
        return Response(serializer.data)
