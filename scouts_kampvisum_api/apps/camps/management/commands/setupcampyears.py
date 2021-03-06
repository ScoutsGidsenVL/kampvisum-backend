from django.core.management.base import BaseCommand


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Sets up the camp years"
    exception = False

    def handle(self, *args, **kwargs):
        from apps.camps.services import CampYearService

        logger.debug("Setting up camp years")
        CampYearService().setup_camp_years()
