from typing import List
import datetime

from django.db import models


from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField
from scouts_auth.groupadmin.models.value_objects import GaAddress

from scouts_auth.inuits.models import AbstractNonModel, Gender, GenderHelper
from scouts_auth.inuits.models.fields import OptionalCharField, OptionalDateField


class GaMemberPersonalData(AbstractNonModel):
    phone_number = OptionalCharField()
    gender: Gender = models.CharField(choices=Gender, default=Gender.UNKNOWN, max_length="1")

    class Meta:
        abstract = True

    def __init__(self, gender: Gender = None, phone_number: str = ""):
        self.gender = gender if gender and isinstance(gender, Gender) else GenderHelper.parse_gender(gender)
        self.phone_number = phone_number

    def __str__(self):
        return "gender({}), phone_number({})".format(self.gender, self.phone_number)


class GaMemberGroupAdminData(AbstractNonModel):
    first_name = OptionalCharField()
    last_name = OptionalCharField()
    birth_date = OptionalDateField()

    class Meta:
        abstract = True

    def __init__(
        self,
        first_name: str = "",
        last_name: str = "",
        birth_date: datetime.date = None,
    ):
        self.first_name = first_name
        self.last_name = last_name

        if isinstance(birth_date, datetime.date):
            self.birth_date = birth_date
        if isinstance(birth_date, str):
            self.birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()

        # super().__init__([], {})

    def __str__(self):
        return "first_name({}), last_name({}), birth_date({})".format(self.first_name, self.last_name, self.birth_date)


class GaProfileMember(AbstractNonModel):
    """Full member profile returned by GA endpoint GET /lid/{id} (GA: volledig profiel van een lid)."""

    personal_data: GaMemberPersonalData
    group_admin_data: GaMemberGroupAdminData
    email: str
    username: str
    group_admin_id = OptionalGroupAdminIdField()
    _inactive_member: bool = False
    addresses: List[GaAddress]

    class Meta:
        abstract = True

    def __init__(
        self,
        personal_data: GaMemberPersonalData = None,
        group_admin_data: GaMemberGroupAdminData = None,
        email: str = "",
        username: str = "",
        group_admin_id: str = "",
        inactive_member: bool = False,
        addresses: List[GaAddress] = None,
    ):
        self.personal_data = personal_data if personal_data else GaMemberPersonalData()
        self.group_admin_data = group_admin_data if group_admin_data else GaMemberGroupAdminData()
        self.email = email
        self.username = username
        self.group_admin_id = group_admin_id
        self._inactive_member = inactive_member
        self.addresses = addresses if addresses else []

    # Necessary for comparison
    @property
    def pk(self):
        return self.group_admin_id

    @property
    def gender(self):
        return self.personal_data.gender

    @property
    def phone_number(self):
        return self.personal_data.phone_number

    @property
    def cell_number(self):
        return self.phone_number

    @property
    def first_name(self):
        return self.group_admin_data.first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self.group_admin_data.first_name = first_name

    @property
    def last_name(self):
        return self.group_admin_data.last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self.group_admin_data.last_name = last_name

    @property
    def birth_date(self):
        return self.group_admin_data.birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        if isinstance(birth_date, datetime.datetime):
            birth_date = birth_date.date()
        self.group_admin_data.birth_date = birth_date

    @property
    def address(self):
        if len(self.addresses) > 0:
            return self.addresses[0]
        return GaAddress()

    @property
    def street(self):
        return self.address.street

    @property
    def number(self):
        return self.address.number

    @property
    def letter_box(self):
        return self.address.letter_box

    @property
    def postal_code(self):
        return self.address.postal_code

    @property
    def city(self):
        return self.address.city

    @property
    def inactive_member(self):
        return self._inactive_member

    @inactive_member.setter
    def inactive_member(self, value: bool):
        self._inactive_member = value

    def __str__(self):
        return (
            self.personal_data.__str__()
            + ", "
            + self.group_admin_data.__str__()
            + ", email({}), username({}), group_admin_id({}), inactive_member ({}), addresses({})"
        ).format(
            self.email,
            self.username,
            self.group_admin_id,
            self.inactive_member,
            ", ".join(str(address) for address in self.addresses) if self.addresses else "[]",
        )
