from scouts_auth.inuits.models import AbstractNonModel
from scouts_auth.inuits.models.fields import OptionalCharField


class GaAddress(AbstractNonModel):
    street = OptionalCharField()
    number = OptionalCharField()
    letter_box = OptionalCharField()
    postal_code = OptionalCharField()
    city = OptionalCharField()

    class Meta:
        abstract = True

    def __init__(
        self,
        street: str = "",
        number: str = "",
        letter_box: str = "",
        postal_code: str = "",
        city: str = "",
    ):
        self.street = street
        self.number = number
        self.letter_box = letter_box
        self.postal_code = postal_code
        self.city = city

    def __str__(self):
        return "street({}), number({}), letter_box({}), postal_code({}), city({})".format(
            self.street,
            self.number,
            self.letter_box,
            self.postal_code,
            self.city,
        )
