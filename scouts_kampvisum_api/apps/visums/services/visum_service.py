from typing import List
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from apps.camps.models import CampType, Camp
from apps.camps.services import CampService, CampTypeService, CampYearService

from apps.deadlines.services import LinkedDeadlineService

from apps.visums.models import LinkedCategorySet, CampVisum, CampVisumEngagement
from apps.visums.services import (
    LinkedCategorySetService,
    InuitsVisumMailService,
    CampVisumEngagementService,
)


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumService:

    year_service = CampYearService()
    camp_type_service = CampTypeService()
    category_set_service = LinkedCategorySetService()
    linked_deadline_service = LinkedDeadlineService()
    mail_service = InuitsVisumMailService()
    visum_engagement_service = CampVisumEngagementService()

    @transaction.atomic
    def visum_create(self, request, **data) -> CampVisum:
        # logger.debug("Creating Campvisum with data: %s", data)

        group = data.get("group", None)
        group_name = data.get("group_name", None)
        year = data.get(
            "year", self.year_service.get_current_camp_year().year)
        name = data.get("name", None)
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        sections = data.get("sections", [])
        camp_types = data.get("camp_types", [])
        engagement: CampVisumEngagement = (
            self.visum_engagement_service.create_engagement()
        )

        logger.debug(
            f"Creating camp '{name}' for group {group.group_admin_id}")

        visum = CampVisum()

        visum.group = group.group_admin_id
        visum.group_name = group_name
        visum.year = year
        visum.name = name
        visum.start_date = start_date
        visum.end_date = end_date
        visum.engagement = engagement
        visum.created_by = request.user

        visum.full_clean()
        visum.save()

        for section in sections:
            visum.sections.add(section)

        visum.full_clean()
        visum.save()

        camp_types: List[CampType] = self.camp_type_service.get_camp_types(
            camp_types=camp_types
        )
        for camp_type in camp_types:
            visum.camp_types.add(camp_type)

        visum.full_clean()
        visum.save()

        logger.debug("Creating LinkedCategorySet for visum %s",
                     visum.name)
        category_set: LinkedCategorySet = (
            self.category_set_service.create_linked_category_set(
                request=request, visum=visum
            )
        )
        visum.category_set = category_set

        visum.full_clean()
        visum.save()

        logger.debug("Linking deadline set to visum")
        self.linked_deadline_service.link_to_visum(
            request=request, visum=visum)

        logger.info(
            "CampVisum created %s (%s)", visum.name, visum.id, user=request.user
        )

        return visum

    @transaction.atomic
    def visum_update(self, request, instance: CampVisum, **fields) -> CampVisum:
        """
        Updates an existing CampVisum object in the DB.
        """
        camp = instance.camp
        camp_fields = fields.pop("camp", None)
        if not camp_fields:
            camp_fields = {}

        camp_types = fields.get("camp_types", None)
        if not camp_types:
            camp_types = instance.camp_types.all()
        else:
            camp_types: List[CampType] = self.camp_type_service.get_camp_types(
                camp_types=camp_types
            )

        logger.debug(
            "Updating camp %s for visum with id %s and camp types (%s)",
            camp.name,
            instance.id,
            ", ".join([camp_type.camp_type for camp_type in camp_types]),
        )

        if not instance.engagement:
            instance.engagement = self.visum_engagement_service.create_engagement()

        instance.camp = self.camp_service.camp_update(
            request, instance=camp, **camp_fields
        )
        instance.updated_by = request.user
        instance.updated_on = timezone.now()
        instance.full_clean()
        instance.save()

        current_camp_types = instance.camp_types.all()
        instance.camp_types.clear()
        for camp_type in camp_types:
            instance.camp_types.add(camp_type)

        logger.debug(
            "Updating LinkedCategorySet with id %s for visum %s (%s)",
            instance.category_set.id,
            instance.camp.name,
            instance.id,
        )
        category_set: LinkedCategorySet = (
            self.category_set_service.update_linked_category_set(
                request=request,
                instance=instance.category_set,
                visum=instance,
                current_camp_types=current_camp_types,
            )
        )

        return instance

    @transaction.atomic
    def delete_visum(self, request, instance: CampVisum):
        logger.debug(
            "Deleting CampVisum with id %s for camp %s", instance.id, instance.camp.name
        )

        camp: Camp = instance.camp
        engagement: CampVisumEngagement = instance.engagement

        self.linked_deadline_service.delete_linked_deadlines_for_visum(
            request=request, visum=instance
        )

        instance.delete()

        if camp:
            camp.delete()
        if engagement:
            engagement.delete()
