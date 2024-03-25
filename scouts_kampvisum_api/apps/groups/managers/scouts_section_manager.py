import logging
from typing import List

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import connections, models
from scouts_auth.auth.exceptions import ScoutsAuthException
from scouts_auth.groupadmin.models import ScoutsFunction, ScoutsGroup
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class ScoutsSectionQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_for_visum(self, visum_id):
        with connections["default"].cursor() as cursor:
            cursor.execute(
                f"select ss.id, ss.name, ss.gender, ss.age_group from groups_scoutssection ss left join visums_campvisum_sections vcs on ss.id = vcs.scoutssection_id where campvisum_id='{visum_id}'"
            )
            return cursor.fetchall()
        return None


class ScoutsSectionManager(models.Manager):
    def get_queryset(self):
        return ScoutsSectionQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        user = kwargs.get("user", None)
        pk = kwargs.get("id", kwargs.get("pk", None))
        name = kwargs.get("name", None)
        gender = kwargs.get("gender", None)
        age_group = kwargs.get("age_group", None)
        # @TODO remove group_group_admin_id
        group = kwargs.get("group", None)
        group_group_admin_id = kwargs.get("group_group_admin_id", None)
        raise_error = kwargs.get("raise_error", False)

        if not user:
            raise ScoutsAuthException(
                "ScoutSection instances can only be access when the authenticated user is provided"
            )

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if name and gender and age_group:
            if group:
                try:
                    return self.get_queryset().get(group=group, name=name, gender=gender, age_group=age_group)
                except Exception:
                    pass

            if group_group_admin_id:
                try:
                    return self.get_queryset().get(
                        group=group_group_admin_id,
                        name=name,
                        gender=gender,
                        age_group=age_group,
                    )
                except Exception:
                    pass

        if raise_error:
            raise ValidationError(
                "Unable to locate ScoutsSection instance with the provided params: (pk: ({}), (group: ({}), name: ({}), gender: ({}), age_group: ({})), (group_group_admin_id: ({}), name ({}), gender({}), age_group({})))".format(
                    pk,
                    group,
                    name,
                    gender,
                    age_group,
                    group_group_admin_id,
                    name,
                    gender,
                    age_group,
                )
            )
        return None

    def get_by_natural_key(self, group, name, gender, age_group):
        logger.trace(
            "GET BY NATURAL KEY %s: (group: %s (%s), name: %s (%s), gender: %s (%s), age_group: %s (%s))",
            "ScoutsSection",
            group,
            type(group).__name__,
            name,
            type(name).__name__,
            gender,
            type(gender).__name__,
            age_group,
            type(age_group).__name__,
        )

        return self.get(group=group, name=name, gender=gender, age_group=age_group)

    def get_for_visum(self, visum_id):
        results = self.get_queryset().get_for_visum(visum_id=visum_id)

        sections = []
        for result in results:
            sections.append(
                {"id": result[0], "name": {"name": result[1], "gender": result[2], "age_group": result[3]}}
            )
        return sections

    def get_for_group(self, group_admin_id: str) -> List:
        return self.get_queryset().filter(group=group_admin_id)
