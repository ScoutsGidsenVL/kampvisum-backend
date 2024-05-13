import typing as tp

from scouts_auth.groupadmin.models.value_objects import AbstractScoutsLink
from scouts_auth.inuits.models import AbstractNonModel


class ScoutsAllowedCalls(AbstractNonModel):
    links: tp.List[AbstractScoutsLink]

    class Meta:
        abstract = True

    def __init__(self, links: tp.List[AbstractScoutsLink] = None):
        self.links = links if links else []

        # super().__init__([], {})

    def __str__(self):
        return "links({})".format(", ".join(link for link in self.links) if self.links else "[]")
