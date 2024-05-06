"""scouts_auth.inuits.serializers.fields.datetime_timezone_serializer_field."""

import pytz
import rest_framework as drf


class DateTimeTimezoneSerializerField(drf.serializers.DateTimeField):
    """Class to make output of a DateTime Field timezone aware"""

    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if value and (not hasattr(value, "tzinfo") or value.tzinfo is None or value.tzinfo.utcoffset(value) is None):
            value = pytz.utc.localize(value)
        return super().to_representation(value)
