"""apps.deadlines.view.deadline_views."""
# LOGGING
import logging

from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.deadlines.models import LinkedDeadline, LinkedDeadlineFlag
from apps.deadlines.serializers import (LinkedDeadlineFlagSerializer,
                                        LinkedDeadlineInputSerializer,
                                        LinkedDeadlineSerializer,
                                        VisumDeadlineSerializer)
from apps.deadlines.services import (LinkedDeadlineFlagService,
                                     LinkedDeadlineService)
from apps.visums.models import CampVisum
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.scouts.permissions import ScoutsFunctionPermissions

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedDeadlineViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedDeadline instances.
    """

    serializer_class = LinkedDeadlineSerializer
    queryset = LinkedDeadline.objects.all()
    permission_classes = (ScoutsFunctionPermissions, )
    filter_backends = [filters.DjangoFilterBackend]

    linked_deadline_service = LinkedDeadlineService()
    linked_deadline_flag_service = LinkedDeadlineFlagService()

    @swagger_auto_schema(
        request_body=LinkedDeadlineInputSerializer,
        responses={status.HTTP_201_CREATED: LinkedDeadlineSerializer},
    )
    def create(self, request):
        """
        Creates a new linked deadline instance.
        """
        logger.debug("LINKED DEADLINE CREATE REQUEST DATA: %s", request.data)
        input_serializer = LinkedDeadlineInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        logger.debug("LINKED DEADLINE CREATE VALIDATED DATA: %s",
                     validated_data)

        instance = self.linked_deadline_service.create_or_update_linked_deadline(
            request, **validated_data
        )

        output_serializer = LinkedDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDeadlineSerializer})
    def retrieve(self, request, pk=None):
        instance: LinkedDeadline = LinkedDeadline.objects.safe_get(
            pk=pk, raise_error=True
        )
        serializer = LinkedDeadlineSerializer(
            instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDeadlineInputSerializer,
        responses={status.HTTP_200_OK: LinkedDeadlineSerializer},
    )
    def partial_update(self, request, pk):
        logger.debug("LINKED DEADLINE UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedDeadline = self.linked_deadline_service.get_linked_deadline(
            linked_deadline_id=pk
        )
        serializer = LinkedDeadlineInputSerializer(
            instance=instance,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("LINKED DEADLINE UPDATE VALIDATED DATA: %s",
                     validated_data)

        instance = self.linked_deadline_service.update_linked_deadline(
            request, instance, **validated_data
        )

        output_serializer = LinkedDeadlineSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDeadlineSerializer})
    def list(self, request):
        """
        Gets all LinkedDeadline instances (filtered).
        """

        instances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: VisumDeadlineSerializer})
    def list_for_visum(self, request, visum_id):
        logger.debug(f"Loading linked deadlines for visum ({visum_id})")

        instances = self.filter_queryset(
            self.linked_deadline_service.list_for_visum(visum=visum_id)
        )
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = VisumDeadlineSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        else:
            serializer = VisumDeadlineSerializer(
                instances, many=True, context={"request": request}
            )
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDeadlineFlagSerializer,
        responses={status.HTTP_200_OK: VisumDeadlineSerializer},
    )
    def partial_update_linked_deadline_flag(
        self, request, linked_deadline_id, linked_deadline_flag_id
    ):
        logger.debug(
            "LINKED DEADLINE FLAG UPDATE REQUEST DATA: %s", request.data)
        instance: LinkedDeadlineFlag = LinkedDeadlineFlag.objects.safe_get(
            id=linked_deadline_flag_id, raise_error=True
        )

        serializer = LinkedDeadlineFlagSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug(
            "LINKED DEADLINE FLAG UPDATE VALIDATED DATA: %s", validated_data)

        instance: LinkedDeadlineFlag = (
            self.linked_deadline_flag_service.update_linked_deadline_flag(
                request, instance, **validated_data
            )
        )

        instance: LinkedDeadline = self.linked_deadline_service.get_visum_deadline(
            linked_deadline=linked_deadline_id
        )
        serializer = VisumDeadlineSerializer(
            instance, context={"request": request})

        return Response(serializer.data)
