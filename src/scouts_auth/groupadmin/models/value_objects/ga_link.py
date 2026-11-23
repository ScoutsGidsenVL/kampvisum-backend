from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class GaLink(AbstractNonModel):
    """This class captures the data returned by GroupAdmin containing links to the full references info."""

    rel = OptionalCharField()
    href = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(self, rel: str = "", href: str = ""):
        self.rel = rel
        self.href = href

    def __str__(self):
        return "rel({}), href({})".format(self.rel, self.href)
