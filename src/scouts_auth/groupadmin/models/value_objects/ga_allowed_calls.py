from typing import List

from scouts_auth.groupadmin.models.value_objects import GaLink
from scouts_auth.inuits.models import AbstractNonModel


class GaAllowedCalls(AbstractNonModel):
    links: List[GaLink]

    class Meta:
        abstract = True

    def __init__(self, links: List[GaLink] = None):
        self.links = links if links else []

        # super().__init__([], {})

    def __str__(self):
        return "links({})".format(", ".join(link for link in self.links) if self.links else "[]")
