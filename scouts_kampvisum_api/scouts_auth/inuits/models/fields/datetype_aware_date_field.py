import datetime as dt
import logging

from django.db import models
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DatetypeAwareDateField(models.DateField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        if isinstance(value, dt.datetime):
            logger.warn("Pythonizing a datetime to a datefield")
            value = value.date()
        return super().to_python(value)
