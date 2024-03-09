"""apps.setup.management.commands.fix93032."""

import logging
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from scouts_auth.inuits.logging import InuitsLogger

from apps.deadlines.models import Deadline

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 93032 https://redmine.inuits.eu/issues/93032"
    exception = True

    @transaction.atomic
    def handle(self, *args, **kwargs):
        deadlines: List[Deadline] = Deadline.objects.all()
        for deadline in deadlines:
            if deadline.name == "camp_registration":
                deadline.is_camp_registration = True

                deadline.full_clean()
                deadline.save()
