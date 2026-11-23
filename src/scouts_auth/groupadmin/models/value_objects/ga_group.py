from typing import List


from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    ListField,
)


class GaGroup(AbstractNonModel):
    """
    Models the scouts groups a user has rights to.

    GA identifies a group by its groepsnummer (e.g. X9010G) everywhere except in the "id" field of
    rest-ga/groep, which holds an internal id. The app keys groups on the groepsnummer only.
    """

    number = OptionalCharField()
    name = OptionalCharField()
    # Kinds of responsibility the logged in user has over this group (GA: verantwoordelijkheden),
    # e.g. "leiding", "algemeen", "regionaal"
    responsibilities = ListField()
    type = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(
        self,
        number: str = "",
        name: str = "",
        responsibilities: List[str] = None,
        type: str = "",
    ):
        self.number = number
        self.name = name
        self.responsibilities = responsibilities if responsibilities else []
        self.type = type

    # Necessary for comparison
    @property
    def pk(self):
        return self.number

    def __str__(self):
        return "number({}), name({}), responsibilities ({}), type({})".format(
            self.number,
            self.name,
            ", ".join(self.responsibilities),
            self.type,
        )
