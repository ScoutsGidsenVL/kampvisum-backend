from django.http.response import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_STRING

from apps.visums.models import CampVisum
from apps.visums.serializers import CampVisumSerializer
from apps.visums.filters import CampVisumFilter
from apps.visums.services import CampVisumService

from scouts_auth.auth.permissions import CustomDjangoPermission

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumViewSet(viewsets.GenericViewSet):
    """
    A viewset for viewing and editing camp instances.
    """

    serializer_class = CampVisumSerializer
    queryset = CampVisum.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CampVisumFilter

    camp_visum_service = CampVisumService()

    def has_group_admin_id() -> bool:
        return True

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_201_CREATED: CampVisumSerializer},
    )
    def create(self, request):
        data = request.data

        logger.debug("CAMP VISUM CREATE REQUEST DATA: %s", data)
        serializer = CampVisumSerializer(
            data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM CREATE VALIDATED DATA: %s", validated_data)

        visum: CampVisum = self.camp_visum_service.visum_create(
            request, **validated_data
        )

        output_serializer = CampVisumSerializer(
            visum, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def retrieve(self, request, pk=None):
        logger.debug(f"Requesting visum {pk}", user=request.user)
        instance = self.get_object()
        logger.debug(f"Visum retrieved: {instance.name}")
        serializer = CampVisumSerializer(
            instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CampVisumSerializer,
        responses={status.HTTP_200_OK: CampVisumSerializer},
    )
    def partial_update(self, request, pk=None):
        instance = self.get_object()

        logger.debug("CAMP VISUM UPDATE REQUEST DATA: %s", request.data)

        serializer = CampVisumSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP VISUM UPDATE VALIDATED DATA: %s", validated_data)

        logger.debug("Updating CampVisum with id %s", pk)

        updated_instance = self.camp_visum_service.visum_update(
            request, instance=instance, **validated_data
        )

        output_serializer = CampVisumSerializer(
            updated_instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def list(self, request):
        group_admin_id = self.request.query_params.get("group", None)
        logger.debug("Listing visums for group %s",
                     group_admin_id, user=request.user)

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        serializer = (
            CampVisumSerializer(page, many=True, context={"request": request})
            if page is not None
            else CampVisumSerializer(instances, many=True, context={"request": request})
        )

        ordered = sorted(
            serializer.data,
            key=lambda k: k.get("sections", [{"age_group": 0}])[0]
            .get("age_group", 0)
            if len(k.get("sections", [{"age_group": 0}])) > 0
            else 0,
        )

        return (
            self.get_paginated_response(ordered)
            if page is not None
            else Response(ordered)
        )

    @swagger_auto_schema(
        responses={status.HTTP_204_NO_CONTENT: Schema(type=TYPE_STRING)}
    )
    def destroy(self, request, pk):
        instance = CampVisum.objects.safe_get(id=pk)

        self.camp_visum_service.delete_visum(
            request=request, instance=instance)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CampVisumSerializer})
    def dates_leaders(self, request, pk=None):
        logger.debug(f"Requesting visum {pk}", user=request.user)
        instance = self.get_object()
        logger.debug(f"Visum retrieved: {instance.name}")
        serializer = CampVisumSerializer(
            instance, context={"request": request})

        for category in serializer.data['category_set']['categories']:
            if category['parent']['name'] == 'planning':
                for sub_category in category['sub_categories']:
                    if sub_category['parent']['name'] == 'planning_date':
                        for check in sub_category['checks']:
                            if check['parent']['name'] == 'planning_date_leaders':
                                return Response(check['value'])
