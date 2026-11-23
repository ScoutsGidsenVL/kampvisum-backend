from datetime import date

from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.inuits.models import AbstractNonModel, Gender


class GaSearchMember(AbstractNonModel):
    """Flat member record, built from a row of the GA member list (POST /ledenlijst/filter/stateless)."""

    group_admin_id = OptionalGroupAdminIdField()
    first_name: str
    last_name: str
    birth_date: date
    email: str
    phone_number: str
    gender: Gender
    inactive_member: bool

    class Meta:
        abstract = True

    def __init__(
        self,
        group_admin_id: str = "",
        first_name: str = "",
        last_name: str = "",
        birth_date: date = None,
        email: str = "",
        phone_number: str = "",
        inactive_member: bool = False,
    ):
        self.group_admin_id = group_admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.inactive_member = inactive_member

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    def __str__(self):
        return "group_admin_id({}), first_name({}), last_name({}), birth_date({}), email({}), phone_number({}), gender ({}), inactive_member ({})".format(
            self.group_admin_id,
            self.first_name,
            self.last_name,
            self.birth_date,
            self.email,
            self.phone_number,
            str(self.gender),
            self.inactive_member,
        )
