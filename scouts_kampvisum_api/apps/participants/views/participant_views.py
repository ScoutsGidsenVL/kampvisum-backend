from asyncio.format_helpers import _format_callback_source
import logging
from typing import List

from django.core.exceptions import ValidationError
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.participants.models import InuitsParticipant
from apps.participants.serializers import InuitsParticipantSerializer
from apps.participants.filters import InuitsParticipantFilter
from apps.participants.services import InuitsParticipantService

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdminMemberService

logger = logging.getLogger(__name__)


class ParticipantViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsParticipantFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsParticipantService()
    groupadmin = GroupAdminMemberService()

    def get_queryset(self):
        return InuitsParticipant.objects.all()

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_201_CREATED: InuitsParticipantSerializer},
    )
    def create(self, request):
        logger.debug("PARTICIPANT CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsParticipantSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("PARTICIPANT CREATE VALIDATED REQUEST DATA: %s", validated_data)

        participant = self.service.create_or_update(
            participant=validated_data, user=request.user
        )

        output_serializer = InuitsParticipantSerializer(
            participant, context={"request": request}
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InuitsParticipantSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsParticipantSerializer,
        responses={status.HTTP_200_OK: InuitsParticipantSerializer},
    )
    def partial_update(self, request, pk=None):
        participant = self.get_object()

        serializer = InuitsParticipantSerializer(
            instance=participant,
            data=request.data,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        participant = self.service.update(
            participant=participant,
            updated_participant=serializer.validated_data,
            updated_by=request.user,
        )

        output_serializer = InuitsParticipantSerializer(participant)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list(self, request):
        participants = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(participants)

        if page is not None:
            serializer = InuitsParticipantSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsParticipantSerializer(participants, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsParticipantSerializer})
    def list_participants(self, request):
        queryset = self.get_queryset()
        participants = self.filter_queryset(queryset)

        output_serializer = InuitsParticipantSerializer(participants, many=True)

        return Response(output_serializer.data)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: InuitsParticipantSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    @action(methods=["get"], detail=False)
    def list_scouts_members(self, request):
        return self._list(request=request, only_scouts_members=True)

    def _list(self, request, include_inactive: bool = False, only_scouts_members=False):
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)

        if not search_term and not group_group_admin_id:
            return self.list_participants(request)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        if not group_group_admin_id:
            logger.debug(
                "Searching for members and non-members with search term %s", search_term
            )
        else:
            logger.debug(
                "Searching for members and non-members with term %s and group %s",
                search_term,
                group_group_admin_id,
            )

        members: List[AbstractScoutsMember] = self.groupadmin.search_member_filtered(
            active_user=request.user,
            term=search_term,
            group_group_admin_id=group_group_admin_id,
        )

        if only_scouts_members:
            results = [
                InuitsParticipant.from_scouts_member(member) for member in members
            ]
        else:
            queryset = self.get_queryset().non_members()
            non_members = self.filter_queryset(queryset)
            results = [
                *[InuitsParticipant.from_scouts_member(member) for member in members],
                *non_members,
            ]

        output_serializer = InuitsParticipantSerializer(results, many=True)

        return Response(output_serializer.data)