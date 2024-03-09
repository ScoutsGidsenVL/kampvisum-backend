"""apps.deadlines.managers.deadline_date_manager."""

import logging

from django.core.exceptions import ValidationError
from django.db import models
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DeadlineDateQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DeadlineDateManager(models.Manager):
    def get_queryset(self):
        return DeadlineDateQuerySet(self.model, using=self._db)

    def safe_get(self, *args, **kwargs):
        pk = kwargs.get("id", kwargs.get("pk", None))
        deadline = kwargs.get("deadline", None)
        raise_error = kwargs.get("raise_error", False)

        if pk:
            try:
                return self.get_queryset().get(pk=pk)
            except Exception:
                pass

        if deadline:
            try:
                return self.get_queryset().get(deadline=deadline)
            except Exception:
                pass

        if raise_error:
            raise ValidationError(
                "Unable to locate DeadlineDate instance(s) with the provided params: (id: {}, deadline: {})".format(
                    pk,
                    deadline,
                )
            )
        return None

    def get_by_natural_key(self, deadline):
        logger.trace(
            "GET BY NATURAL KEY %s: (deadline: %s (%s))",
            "DeadlineDate",
            deadline,
            type(deadline).__name__,
        )

        return self.get(deadline=deadline)
