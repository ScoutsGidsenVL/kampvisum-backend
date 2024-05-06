"""scouts_auth.inuits.exceptions.db_not_ready."""

from django.db.utils import DatabaseError


class DbNotReadyException(DatabaseError):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
