"""apps.setup.management.commands.empty_functions_groups."""

import logging
from typing import List

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.models import Q
from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsUser
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Truncate the function and group tables"
    exception = True

    @transaction.atomic
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("truncate table scouts_auth_scoutsfunction")
            cursor.execute("truncate table scouts_auth_scoutsgroup")
