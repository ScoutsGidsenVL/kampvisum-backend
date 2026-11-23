from typing import List

from scouts_auth.groupadmin.models.value_objects import GaLink
from scouts_auth.inuits.models import AbstractNonModel


class GaPage(AbstractNonModel):
    """
    Class to capture composite responses, that typically contain a list of links and a list of objects.
    """

    links: List[GaLink] = []

    class Meta:
        abstract = True

    def __init__(self, links: List[GaLink] = None):
        self.links = links if links else []

    def __str__(self):
        return "links: ({})".format(", ".join(str(link) for link in self.links) if self.links else "[]")
