from datetime import datetime, date
import re


class DateUtils:
    @staticmethod
    def datetime_from_isoformat(datetime_string: str = None) -> datetime:
        if not datetime_string:
            return None
        return datetime.fromisoformat(re.sub("\.[0-9]+", "", datetime_string))

    @staticmethod
    def date_from_isoformat(datetime_string: str = None) -> date:
        if not datetime_string:
            return None
        return DateUtils.datetime_from_isoformat(datetime_string).date()
