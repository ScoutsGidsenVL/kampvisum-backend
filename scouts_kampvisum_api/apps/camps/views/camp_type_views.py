"""apps.camps.views.camp_type_views."""
# LOGGING
import logging

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from drf_yasg.openapi import TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from apps.camps.models import CampType
from apps.camps.serializers import CampTypeSerializer
from apps.camps.services import CampTypeService
from scouts_auth.auth.permissions import CustomDjangoPermission
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions

logger: InuitsLogger = logging.getLogger(__name__)


class CampTypeViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing CampType instances.
    """

    serializer_class = CampTypeSerializer
    queryset = CampType.objects.all().selectable()
    permission_classes = (ScoutsFunctionPermissions, )

    camp_type_service = CampTypeService()

    @swagger_auto_schema(
        request_body=CampTypeSerializer,
        responses={status.HTTP_201_CREATED: CampTypeSerializer},
    )
    def create(self, request):
        """
        Creates a new CampType instance.
        """
        # logger.debug("CAMP TYPE CREATE REQUEST DATA: %s", request.data)
        input_serializer = CampTypeSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        # logger.debug("CAMP TYPE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.camp_type_service.create(request, **validated_data)

        output_serializer = CampTypeSerializer(
            instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampTypeSerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a CampType instance from the db.
        """

        instance = self.get_object()
        serializer = CampTypeSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampTypeSerializer,
        responses={status.HTTP_200_OK: CampTypeSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a CampType instance.
        """

        instance = self.get_object()

        # logger.debug("CAMP TYPE UPDATE REQUEST DATA: %s", request.data)
        serializer = CampTypeSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        # logger.debug("CAMP TYPE UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.camp_type_service.update(
            request, instance=instance, **validated_data
        )

        output_serializer = CampTypeSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def delete(self, request, pk):
        """
        Deletes a CampType instance.
        """

        instance = get_object_or_404(CampType.objects, pk=pk)
        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampTypeSerializer})
    def list(self, request):
        """
        Gets all CampType instances (filtered).
        """

        instances = self.filter_queryset(self.queryset)
        #instances = CampType.objects.all()
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = CampTypeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CampTypeSerializer(instances, many=True)
            return Response(serializer.data)
