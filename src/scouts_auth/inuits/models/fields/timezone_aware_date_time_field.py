from datetime import timezone

from django.db import models


class TimezoneAwareDateTimeField(models.DateTimeField):
    """Class to make output of a DateTime Field timezone aware"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value and (not hasattr(value, "tzinfo") or value.tzinfo is None or value.tzinfo.utcoffset(value) is None):
            value = value.replace(tzinfo=timezone.utc)
        return super().to_python(value)
