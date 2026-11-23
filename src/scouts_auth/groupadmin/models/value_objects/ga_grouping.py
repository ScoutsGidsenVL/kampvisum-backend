from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class GaGrouping(AbstractNonModel):
    name = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(self, name: str = ""):
        self.name = name

    def __str__(self):
        return "name({})".format(self.name)
