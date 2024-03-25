"""apps.setup.management.commands.createvisums."""

import logging
import re
from types import SimpleNamespace
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsToken, ScoutsUser
from scouts_auth.inuits.logging import InuitsLogger
from scouts_auth.scouts.services import ScoutsUserSessionService

from apps.groups.models import ScoutsSection
from apps.visums.models import CampVisum
from apps.visums.services import CampVisumService

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates the specified amount of test visums for each of the user's scouts groups"
    exception = True

    visum_service = CampVisumService()
    sections: dict = {}

    default_count = 10
    default_start = 0
    re_bearer = re.compile(re.escape("bearer"), re.IGNORECASE)

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--count",
            type=int,
            dest="count",
            default=self.default_count,
            help="Number of visums to create for each group",
        )
        parser.add_argument(
            "-s",
            "--start",
            type=int,
            dest="start",
            default=self.default_start,
            help="Index to start counting from",
        )
        parser.add_argument(
            "-t",
            "--token",
            type=str,
            dest="access_token",
            default="",
            help="Valid and active access token to retrieve a scouts user",
        )

    # fix for https://redmine.inuits.eu/issues/91782 for functions that had too many groups
    @transaction.atomic
    def handle(self, *args, **options):
        count: int = options.get("count", self.default_count)
        start: int = options.get("start", self.default_start)
        access_token: str = options.get("access_token", None)

        if not count or not access_token:
            return

        access_token = self.re_bearer.sub("", access_token)

        user: ScoutsUser = ScoutsUserSessionService.get_user_from_session(
            access_token=ScoutsToken.from_access_token(access_token)
        )
        if not user:
            raise ScoutsAuthException("Unable to find user with provided access token")

        scouts_groups = user.get_scouts_groups()
        for group_count in range(1, len(scouts_groups)):
            scouts_group = scouts_groups[group_count]
            for x in range(start, start + count):
                data: dict = {
                    "group": scouts_group.group_admin_id,
                    "group_name": scouts_group.name,
                    "name": f"INUITS speed test {scouts_group.group_admin_id} {x:03}",
                    "sections": [self.get_next_section(group_admin_id=scouts_group.group_admin_id, index=x - start)],
                }

                visum: CampVisum = self.visum_service.visum_create(request=SimpleNamespace(user=user), **data)

                logger.debug(f"Created visum {visum.name} for group {visum.group}")

    def get_next_section(self, group_admin_id: str, index: int) -> ScoutsSection:
        if group_admin_id not in self.sections:
            self.sections[group_admin_id] = ScoutsSection.objects.get_for_group(group_admin_id=group_admin_id)

        if index > len(self.sections[group_admin_id]):
            index = index - len(self.sections[group_admin_id])

        return self.sections[group_admin_id][index]
