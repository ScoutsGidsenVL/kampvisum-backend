"""apps.setup.management.commands.sprint7fix91022."""

import logging
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from scouts_auth.inuits.logging import InuitsLogger

from apps.groups.services import DefaultScoutsSectionNameService
from apps.visums.models import CampVisum, CampVisumEngagement

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fixes issue 92074 https://redmine.inuits.eu/issues/92074"
    exception = True

    default_section_name_service = DefaultScoutsSectionNameService()

    BASE_PATH = "apps/groups/fixtures"
    DEFAULT_SECTION_NAMES = "default_scouts_section_names.json"

    # fix for https://redmine.inuits.eu/issues/92074 for groups that were already registered
    @transaction.atomic
    def handle(self, *args, **kwargs):
        visums: List[CampVisum] = CampVisum.objects.all()

        for visum in visums:
            if not visum.engagement:
                engagement = CampVisumEngagement()
                engagement.full_clean()
                engagement.save()

                visum.engagement = engagement

                visum.full_clean()
                visum.save()
