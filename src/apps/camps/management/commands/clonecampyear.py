from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from apps.camps.services import CampYearCloneService


import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Clones the previous camp year's categories, sub-categories, checks and "
        "deadlines into the current camp year. Takes no arguments: the current camp "
        "year is computed the same way as everywhere else in the application. Only "
        "creates what the current camp year lacks, so a half-finished clone can be run "
        "again. Archived rows are not cloned."
    )
    exception = False

    def handle(self, *args, **kwargs):
        try:
            message, cloned = CampYearCloneService().clone_to_current_year()
        except ValidationError as error:
            raise CommandError(" ".join(error.messages)) from error

        if cloned:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.WARNING(message))
