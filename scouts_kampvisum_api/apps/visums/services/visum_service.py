from typing import List

from django.db import transaction

from apps.camps.models import CampType
from apps.camps.services import CampService, CampTypeService

from apps.deadlines.services import LinkedDeadlineService

from apps.visums.models import LinkedCategorySet, CampVisum
from apps.visums.services import LinkedCategorySetService, InuitsVisumMailService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumService:

    camp_service = CampService()
    camp_type_service = CampTypeService()
    category_set_service = LinkedCategorySetService()
    linked_deadline_service = LinkedDeadlineService()
    mail_service = InuitsVisumMailService()

    @transaction.atomic
    def visum_create(self, request, **data) -> CampVisum:
        logger.debug("Creating Campvisum with data: %s", data)

        camp_data = data.get("camp", {})
        camp_name = camp_data.get("name", None)

        logger.debug("Creating camp with name '%s'", camp_name)
        camp = self.camp_service.camp_create(request, **camp_data)

        camp_types: List[CampType] = self.camp_type_service.get_camp_types(
            camp_types=data.get("camp_types")
        )

        logger.debug(
            "Creating CampVisum instance for camp %s with camp type(s) (%s)",
            camp.name,
            ",".join(camp_type.camp_type for camp_type in camp_types),
        )

        visum = CampVisum()

        visum.camp = camp
        visum.created_by = request.user

        visum.full_clean()
        visum.save()

        for camp_type in camp_types:
            visum.camp_types.add(camp_type)

        visum.full_clean()
        visum.save()

        logger.debug("Creating LinkedCategorySet for visum %s", visum.camp.name)
        category_set: LinkedCategorySet = (
            self.category_set_service.create_linked_category_set(
                request=request, visum=visum
            )
        )

        logger.debug("Linking deadline set to visum")
        self.linked_deadline_service.link_to_visum(request=request, visum=visum)

        self.mail_service.notify_camp_registered(visum=visum)

        return visum

    @transaction.atomic
    def visum_update(self, request, instance: CampVisum, **fields) -> CampVisum:
        """
        Updates an existing CampVisum object in the DB.
        """
        camp = instance.camp
        camp_fields = fields.pop("camp")

        camp_types = fields.get("camp_types", [])
        camp_types: List[CampType] = self.camp_type_service.get_camp_types(
            camp_types=camp_types
        )

        logger.debug("Updating camp %s for visum with id %s", camp.name, instance.id)
        instance.camp = self.camp_service.camp_update(
            request, instance=camp, **camp_fields
        )

        logger.debug(
            "Updating LinkedCategorySet with id %s for visum with id %s",
            instance.category_set.id,
            instance.id,
        )
        category_set: LinkedCategorySet = (
            self.category_set_service.update_linked_category_set(
                request=request,
                instance=instance.category_set,
                visum=instance,
            )
        )

        instance.full_clean()
        instance.save()

        # existing_camp_types = instance.category_set.parent.camp_type
        camp_types = fields.get("camp_types", [])

        return instance
