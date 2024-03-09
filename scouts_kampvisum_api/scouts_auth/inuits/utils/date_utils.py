import datetime as dt


class DateUtils:
    @staticmethod
    def datetime_from_isoformat(datetime_string: str = None) -> dt.datetime:
        if not datetime_string:
            return None
        return dt.datetime.fromisoformat(datetime_string)

    @staticmethod
    def date_from_isoformat(datetime_string: str = None) -> dt.date:
        if not datetime_string:
            return None
        return DateUtils.datetime_from_isoformat(datetime_string).date()
