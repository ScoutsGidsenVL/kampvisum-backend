from django.core.management.base import BaseCommand

from apps.camps.services import CampYearCloneService


import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Clones the previous camp year's categories, sub-categories, checks and "
        "deadlines into the current camp year. Takes no arguments: the current camp "
        "year is computed the same way as everywhere else in the application. Does "
        "nothing (with a warning) if the current camp year already has categories, or "
        "if the previous camp year has none to clone from."
    )
    exception = False

    def handle(self, *args, **kwargs):
        message, cloned = CampYearCloneService().clone_to_current_year()

        if cloned:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.WARNING(message))
