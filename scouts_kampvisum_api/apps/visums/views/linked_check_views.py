import logging
from typing import List

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.visums.models import (
    CheckType,
    CheckTypeEndpoint,
    LinkedCheck,
    LinkedSimpleCheck,
    LinkedDateCheck,
    LinkedDurationCheck,
    LinkedLocationCheck,
    LinkedMemberCheck,
    LinkedFileUploadCheck,
    LinkedCommentCheck,
)
from apps.visums.serializers import (
    LinkedCheckSerializer,
    LinkedSimpleCheckSerializer,
    LinkedDateCheckSerializer,
    LinkedDurationCheckSerializer,
    LinkedLocationCheckSerializer,
    LinkedCampLocationCheckSerializer,
    LinkedMemberCheckSerializer,
    LinkedFileUploadCheckSerializer,
    LinkedCommentCheckSerializer,
)
from apps.visums.services import LinkedCheckService

from scouts_auth.inuits.serializers import PersistedFileSerializer


logger = logging.getLogger(__name__)


class LinkedCheckViewSet(viewsets.GenericViewSet):
    """
    A viewset for LinkedCheck instances.
    """

    serializer_class = LinkedCheckSerializer
    queryset = LinkedCheck.objects.all()
    filter_backends = [filters.DjangoFilterBackend]

    linked_check_service = LinkedCheckService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve(self, request, pk=None):
        instance: LinkedCheck = get_object_or_404(LinkedCheck.objects, pk=pk)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def retrieve_simple_check(self, request, check_id=None):
        instance: LinkedCheck = self.linked_check_service.get_simple_check(check_id)
        serializer = LinkedCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedSimpleCheckSerializer,
        responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer},
    )
    def partial_update_simple_check(self, request, check_id):
        instance = self.linked_check_service.get_simple_check(check_id)

        logger.debug("SIMPLE CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedSimpleCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("SIMPLE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_simple_check(
            instance, **validated_data
        )

        output_serializer = LinkedSimpleCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDateCheckSerializer})
    def retrieve_data_check(self, request, check_id=None):
        instance: LinkedDateCheck = self.linked_check_service.get_date_check(check_id)
        serializer = LinkedDateCheckSerializer(instance, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDateCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDateCheckSerializer},
    )
    def partial_update_date_check(self, request, check_id):
        instance = self.linked_check_service.get_date_check(check_id)

        logger.debug("DATE CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedDateCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DATE CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_date_check(
            instance, **validated_data
        )

        output_serializer = LinkedDateCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDurationCheckSerializer})
    def retrieve_duration_check(self, request, check_id=None):
        instance: LinkedDurationCheck = self.linked_check_service.get_duration_check(
            check_id
        )
        serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedDurationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedDurationCheckSerializer},
    )
    def partial_update_duration_check(self, request, check_id):
        instance = self.linked_check_service.get_duration_check(check_id)

        logger.debug("DURATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedDurationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("DURATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_duration_check(
            instance, **validated_data
        )

        output_serializer = LinkedDurationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def retrieve_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = self.linked_check_service.get_location_check(
            check_id
        )
        serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedLocationCheckSerializer},
    )
    def partial_update_location_check(self, request, check_id):
        instance = self.linked_check_service.get_location_check(check_id)

        logger.debug("LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def retrieve_camp_location_check(self, request, check_id=None):
        instance: LinkedLocationCheck = (
            self.linked_check_service.get_camp_location_check(check_id)
        )
        serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCampLocationCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer},
    )
    def partial_update_camp_location_check(self, request, check_id):
        instance = self.linked_check_service.get_camp_location_check(check_id)

        logger.debug("CAMP LOCATION CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedCampLocationCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CAMP LOCATION CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_camp_location_check(
            instance, **validated_data
        )

        output_serializer = LinkedCampLocationCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def retrieve_file_upload_check(self, request, check_id=None):
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )
        serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedFileUploadCheckSerializer,
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer},
    )
    def partial_update_file_upload_check(self, request, check_id):
        instance: LinkedFileUploadCheck = (
            self.linked_check_service.get_file_upload_check(check_id)
        )

        logger.debug("FILE UPLOAD CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = PersistedFileSerializer(
            data=request.data, context={"request": request}
        )
        # serializer = LinkedFileUploadCheckSerializer(
        #     data=request.data,
        #     instance=instance,
        #     context={"request": request},
        #     partial=True,
        # )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("FILE UPLOAD CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_file_upload_check(
            instance=instance, uploaded_file=validated_data.get("file")
        )

        output_serializer = LinkedFileUploadCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCommentCheckSerializer})
    def retrieve_comment_check(self, request, check_id=None):
        instance: LinkedCommentCheck = self.linked_check_service.get_comment_check(
            check_id
        )
        serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=LinkedCommentCheckSerializer,
        responses={status.HTTP_200_OK: LinkedCommentCheckSerializer},
    )
    def partial_update_comment_check(self, request, check_id):
        instance = self.linked_check_service.get_comment_check(check_id)

        logger.debug("COMMENT CHECK UPDATE REQUEST DATA: %s", request.data)
        serializer = LinkedCommentCheckSerializer(
            data=request.data,
            instance=instance,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("COMMENT CHECK UPDATE VALIDATED DATA: %s", validated_data)

        instance = self.linked_check_service.update_comment_check(
            instance, **validated_data
        )

        output_serializer = LinkedCommentCheckSerializer(
            instance, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def _list(self, instances: List[LinkedCheck]):
        page = self.paginate_queryset(instances)

        if page is not None:
            serializer = LinkedCheckSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = LinkedCheckSerializer(instances, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCheckSerializer})
    def list(self, request):
        """
        Gets all Check instances (filtered).
        """

        return self._list(instances=self.filter_queryset(self.get_queryset()))

    @action(
        detail=False,
        methods=["get"],
        url_path=r"simple",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedSimpleCheckSerializer})
    def list_simple_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.SIMPLE_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"date",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDateCheckSerializer})
    def list_date_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.DATE_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"duration",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedDurationCheckSerializer})
    def list_duration_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.DURATION_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"location",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedLocationCheckSerializer})
    def list_location_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.LOCATION_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"camp_location",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedCampLocationCheckSerializer}
    )
    def list_camp_location_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.CAMP_LOCATION_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"member",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedMemberCheckSerializer})
    def list_member_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.MEMBER_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"file",
    )
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: LinkedFileUploadCheckSerializer}
    )
    def list_file_upload_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.FILE_UPLOAD_CHECK
            )
        )

    @action(
        detail=False,
        methods=["get"],
        url_path=r"comment",
    )
    @swagger_auto_schema(responses={status.HTTP_200_OK: LinkedCommentCheckSerializer})
    def list_comment_checks(self, request):
        return self._list(
            self.get_queryset().filter(
                parent__check_type__check_type=CheckTypeEndpoint.COMMENT_CHECK
            )
        )
