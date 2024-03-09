import datetime as dt
import logging

import pytz
from rest_framework import serializers

from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class DatetypeAndTimezoneAwareDateTimeSerializerField(serializers.DateTimeField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, value):
        if not value:
            return None

        if isinstance(value, dt.date):
            # logger.warn(
            #     "Field %s: Received a date value for a datetime field, transforming to datetime",
            #     self.field_name,
            # )
            value = dt.datetime.combine(value, dt.datetime.min.time())

        return super().to_internal_value(value)

    def to_representation(self, value):
        if not value:
            return None

        if not isinstance(value, dt.datetime):
            # logger.warn(
            #     "Field %s: Attempting to serialize a date value for a datetime field, transforming to datetime",
            #     self.field_name,
            # )
            value = dt.datetime.combine(value, dt.datetime.min.time())

        if not hasattr(value, "tzinfo") or value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            # logger.warn(
            #     "Field %s: Attempting to serialize a datetime value that does not have timzone info", self.field_name
            # )
            value = pytz.utc.localize(value)

        return super().to_representation(value)
