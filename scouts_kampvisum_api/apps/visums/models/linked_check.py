import logging

from django.db import models
from django.core.exceptions import ValidationError

from apps.visums.models import (
    LinkedSubCategory,
    VisumCheck,
    CheckType,
    VisumCheck,
    CheckType,
)
from apps.visums.models.enums import CheckState

from scouts_auth.inuits.models import AbstractBaseModel, PersistedFile
from scouts_auth.inuits.models.fields import (
    DefaultCharField,
    OptionalCharField,
    DatetypeAwareDateField,
)


logger = logging.getLogger(__name__)


class LinkedCheck(AbstractBaseModel):

    parent = models.ForeignKey(VisumCheck, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
    )

    # Hackety hack ?
    def get_value_type(self):
        concrete_type = LinkedCheck.get_concrete_check_type(self.parent)

        check = concrete_type.__class__.objects.get(linkedcheck_ptr=self.id)
        logger.debug("CONCRETE CHECK: %s", check)

        return check

    @staticmethod
    def get_concrete_check_type(check: VisumCheck):
        check_type: CheckType = check.check_type

        if check_type.is_simple_check():
            return LinkedSimpleCheck()
        elif check_type.is_date_check():
            return LinkedDateCheck()
        elif check_type.is_duration_check():
            return LinkedDurationCheck()
        elif check_type.is_location_check():
            return LinkedLocationCheck()
        elif check_type.is_location_contact_check():
            return LinkedLocationContactCheck()
        elif check_type.is_member_check():
            return LinkedMemberCheck()
        elif check_type.is_contact_check():
            return LinkedContactCheck()
        elif check_type.is_file_upload_check():
            return LinkedFileUploadCheck()
        elif check_type.is_input_check():
            return LinkedInputCheck()
        elif check_type.is_information_check():
            return LinkedInformationCheck()
        else:
            raise ValidationError(
                "Check type {} is not recognized".format(check_type.check_type)
            )


# ##############################################################################
# LinkedSimpleCheck
#
# A check that can be checked, unchecked or set as not applicable
# ##############################################################################
class LinkedSimpleCheck(LinkedCheck):
    value = DefaultCharField(choices=CheckState.choices, default=CheckState.UNCHECKED)


# ##############################################################################
# LinkedDateCheck
#
# A check that contains a date
# ##############################################################################
class LinkedDateCheck(LinkedCheck):
    value = DatetypeAwareDateField(null=True, blank=True)


# ##############################################################################
# LinkedDurationCheck
#
# A check that contains a start and end date
# ##############################################################################
class LinkedDurationCheck(LinkedCheck):
    start_date = DatetypeAwareDateField(null=True, blank=True)
    end_date = DatetypeAwareDateField(null=True, blank=True)


# ##############################################################################
# LinkedLocationCheck
#
# A check that contains a geo-coordinate
# ##############################################################################
class LinkedLocationCheck(LinkedCheck):
    # @TODO
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedLocationContactCheck
#
# A check that contains a geo-coordinate and contact details
# ##############################################################################
class LinkedLocationContactCheck(LinkedCheck):
    # @TODO
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedMemberCheck
#
# A check that selects members and non-members
# ##############################################################################
class LinkedMemberCheck(LinkedCheck):
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedContactCheck
#
# A check that contains contact information
# ##############################################################################
class LinkedContactCheck(LinkedCheck):
    value = OptionalCharField(max_length=64)


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
class LinkedFileUploadCheck(LinkedCheck):
    value = models.OneToOneField(
        PersistedFile, on_delete=models.CASCADE, null=True, blank=True
    )


# ##############################################################################
# LinkedInputCheck
#
# A check that contains text
# ##############################################################################
class LinkedInputCheck(LinkedCheck):
    value = OptionalCharField(max_length=300)


# ##############################################################################
# LinkedInformationCheck
#
# A check that contains extra information as text
# ##############################################################################
class LinkedInformationCheck(LinkedInputCheck):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
