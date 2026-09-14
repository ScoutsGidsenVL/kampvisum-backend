from types import SimpleNamespace
from typing import List

from django.core.management.base import BaseCommand

from apps.camps.models import CampYear
from apps.camps.services import CampYearService

from apps.visums.models import CampVisum
from apps.visums.services import CampVisumService


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates existing visums of the current camp year to match the current category, sub-category and check structure"
    exception = False

    camp_visum_service = CampVisumService()

    def handle(self, *args, **kwargs):
        from scouts_auth.groupadmin.models import ScoutsUser

        current_camp_year: CampYear = CampYearService().get_or_create_current_camp_year()
        visums: List[CampVisum] = list(CampVisum.objects.all().filter(year=current_camp_year))

        for visum in visums:
            self.camp_visum_service.visum_update(
                request=SimpleNamespace(user=ScoutsUser.objects.safe_get(username="FIXTURES")), instance=visum, **{}
            )
