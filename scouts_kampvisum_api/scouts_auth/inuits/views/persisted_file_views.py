import logging
from http.client import NOT_FOUND

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.openapi import TYPE_STRING, Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from apps.visums.models import LinkedCheck
from scouts_auth.inuits.filters import PersistedFileFilter
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.inuits.models import PersistedFile
from scouts_auth.inuits.serializers import PersistedFileDetailedSerializer, PersistedFileSerializer
from scouts_auth.inuits.services import PersistedFileService
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions
from scouts_auth.scouts.services import ScoutsPermissionService

logger: InuitsLogger = logging.getLogger(__name__)


class PersistedFileViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing PersistedFile instances.
    """

    serializer_class = PersistedFileSerializer
    permission_classes = (ScoutsFunctionPermissions,)
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = PersistedFileFilter

    persisted_file_service = PersistedFileService()
    authorization_service = ScoutsPermissionService()

    def get_queryset(self):
        return PersistedFile.objects.allowed(group=self.request.GET.get("group"))

    @swagger_auto_schema(
        request_body=PersistedFileSerializer,
        responses={status.HTTP_201_CREATED: PersistedFileSerializer},
    )
    def create(self, request):
        """
        Creates a new PersistedFile instance.
        """
        logger.debug("PERSISTED FILE CREATE REQUEST DATA: %s", request.data)
        input_serializer = PersistedFileSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PERSISTED FILE CREATE VALIDATED DATA: %s", validated_data)

        instance = self.persisted_file_service.save(request, validated_data)

        output_serializer = PersistedFileSerializer(instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersistedFileSerializer})
    def retrieve(self, request, pk=None):
        """
        Gets and returns a PersistedFile instance from the db.
        """
        try:
            instance = self.get_object(pk)
        except PersistedFile.DoesNotExist:
            raise NOT_FOUND("PersistedFile not found.")
        except PersistedFile.MultipleObjectsReturned:
            # This should not happen if the primary key is unique.
            raise Exception("Multiple PersistedFile objects returned for the same primary key.")

        serializer = PersistedFileDetailedSerializer(instance, context={"request": request})

        return Response(serializer.data)

    def get_object(self, pk):
        return PersistedFile.objects.filter(pk=pk).get()

    @swagger_auto_schema(
        request_body=PersistedFileSerializer,
        responses={status.HTTP_200_OK: PersistedFileSerializer},
    )
    def partial_update(self, request, pk=None):
        """
        Updates a PersistedFile instance.
        """

        instance = self.get_object()
        logger.debug("PERSISTED FILE UPDATE REQUEST DATA: %s", request.data)
        serializer = PersistedFileSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("PERSISTED FILE UPDATE VALIDATED DATA: %s", validated_data)

        updated_instance = self.persisted_file_service.update(request, instance=instance, **validated_data)

        output_serializer = PersistedFileSerializer(updated_instance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)})
    def delete(self, request, pk):
        """
        Deletes a PersistedFile instance.
        """
        instance: PersistedFile = get_object_or_404(PersistedFile.objects, pk=pk)
        logger.debug(
            "Deleting PersistedFile instance with id %s and name %s",
            instance.id,
            instance.file.name,
        )

        instance.delete()

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersistedFileSerializer})
    def list(self, request):
        """
        Gets all PersistedFile instances (filtered).
        """
        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = PersistedFileSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = PersistedFileSerializer(instances, many=True)
            return Response(serializer.data)
