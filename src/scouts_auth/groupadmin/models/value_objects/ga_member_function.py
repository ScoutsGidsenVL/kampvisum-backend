from datetime import datetime

from scouts_auth.groupadmin.models.value_objects import GaGroup
from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField

from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalDateTimeField,
)


class GaMemberFunction(AbstractNonModel):
    """
    A function exercised by a member in a group (GA: functie-instantie).
    Has an end date when the function ended. See GaFunctionDescription for the function type catalog.
    """

    function = OptionalGroupAdminIdField()
    end = OptionalDateTimeField()

    code = OptionalCharField()
    description = OptionalCharField()

    # Declare as foreign keys in concrete subclasses
    scouts_group: GaGroup = None

    class Meta:
        abstract = True

    def __init__(
        self,
        scouts_group: GaGroup = None,
        function: str = None,
        end: datetime = None,
        code: str = None,
        description: str = None,
    ):
        self.function = function
        self.scouts_group = scouts_group
        self.end = end
        self.code = code
        self.description = description

    # Necessary for comparison
    @property
    def pk(self):
        return self.function

    def __str__(self):
        return "function({}), scouts_group({}), end ({}), code({}), description({})".format(
            self.function,
            str(self.scouts_group),
            self.end,
            self.code,
            self.description,
        )
