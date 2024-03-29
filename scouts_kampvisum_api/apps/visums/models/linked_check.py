import datetime

from django.db import models
from django.core.exceptions import ValidationError

from apps.locations.models import LinkedLocation

from apps.participants.models import VisumParticipant
from apps.participants.models.enums import ParticipantType

from apps.visums.models import (
    LinkedSubCategory,
    Check,
    CheckType,
)
from apps.visums.models.enums import CheckState
from apps.visums.managers import LinkedCheckManager
from apps.visums.utils import CheckValidator

from scouts_auth.inuits.models import AuditedArchiveableBaseModel, PersistedFile
from scouts_auth.inuits.models.fields import (
    DefaultCharField,
    OptionalCharField,
    OptionalIntegerField,
    DefaultIntegerField,
    DatetypeAwareDateField,
)

# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class LinkedCheck(AuditedArchiveableBaseModel):

    objects = LinkedCheckManager()

    parent = models.ForeignKey(Check, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        LinkedSubCategory, on_delete=models.CASCADE, related_name="checks"
    )
    check_state = DefaultCharField(
        choices=CheckState.choices,
        default=CheckState.UNCHECKED,
        max_length=32
    )

    class Meta:
        ordering = ["parent__index"]

    def is_required_for_validation(self) -> bool:
        return self.parent.is_required_for_validation

    def should_be_checked(self) -> bool:
        return self.parent.check_type.should_be_checked()

    def is_checked(self) -> bool:
        if self.should_be_checked():
            return self.has_value()
        return True

    def get_value_type(self):
        concrete_type = LinkedCheck.get_concrete_check_type(self.parent)

        check = concrete_type.__class__.objects.get(linkedcheck_ptr=self.id)

        return check

    def validate_value(self, value: any):
        if self.parent.validators:
            if not CheckValidator.validate(self.parent.validators, value):
                raise ValidationError(
                    f"LinkedCheck does not validate: {value}")

        return True

    @staticmethod
    def get_concrete_check_type_by_id(check_id):
        return LinkedCheck.get_concrete_check_type(Check.objects.safe_get(pk=check_id))

    @staticmethod
    def get_concrete_check_type(check: Check):
        check_type: CheckType = check.check_type

        if check_type.is_simple_check():
            return LinkedSimpleCheck()
        elif check_type.is_date_check():
            return LinkedDateCheck()
        elif check_type.is_duration_check():
            return LinkedDurationCheck()
        elif check_type.is_location_check():
            return LinkedLocationCheck()
        elif check_type.is_camp_location_check():
            return LinkedLocationCheck(is_camp_location=True)
        elif check_type.is_participant_adult_check():
            return LinkedParticipantCheck(participant_check_type=ParticipantType.ADULT)
        elif check_type.is_participant_responsible_check():
            return LinkedParticipantCheck(
                participant_check_type=ParticipantType.RESPONSIBLE
            )
        elif check_type.is_participant_leader_check():
            return LinkedParticipantCheck(participant_check_type=ParticipantType.LEADER)
        elif check_type.is_participant_cook_check():
            return LinkedParticipantCheck(participant_check_type=ParticipantType.COOK)
        elif check_type.is_participant_member_check():
            return LinkedParticipantCheck(participant_check_type=ParticipantType.MEMBER)
        elif check_type.is_participant_check():
            return LinkedParticipantCheck(
                participant_check_type=ParticipantType.PARTICIPANT
            )
        elif check_type.is_file_upload_check():
            return LinkedFileUploadCheck()
        elif check_type.is_comment_check():
            return LinkedCommentCheck()
        elif check_type.is_number_check():
            return LinkedNumberCheck()
        else:
            raise ValidationError(
                "Check type {} is not recognized".format(check_type.check_type)
            )

    @property
    def readable_name(self):
        return "{}".format(self.parent.name)


# ##############################################################################
# LinkedSimpleCheck
#
# A check that can be checked, unchecked or set as not applicable
# ##############################################################################
class LinkedSimpleCheck(LinkedCheck):
    value = DefaultCharField(choices=CheckState.choices,
                             default=CheckState.EMPTY)

    def has_value(self) -> bool:
        if CheckState.is_checked_or_irrelevant(self.value) and self.validate_value(self.value):
            return True
        return False


# ##############################################################################
# LinkedDateCheck
#
# A check that contains a date
# ##############################################################################
class LinkedDateCheck(LinkedCheck):
    value = DatetypeAwareDateField(null=True, blank=True)

    def has_value(self) -> bool:
        if self.value and self.validate_value(self.value):
            return True
        return False


# ##############################################################################
# LinkedDurationCheck
#
# A check that contains a start and end date
# ##############################################################################
class LinkedDurationCheck(LinkedCheck):
    start_date = DatetypeAwareDateField(null=True, blank=True)
    end_date = DatetypeAwareDateField(null=True, blank=True)

    def has_value(self) -> bool:
        if self.start_date and self.end_date:
            return True
        return False


# ##############################################################################
# LinkedLocationCheck
#
# A check that contains a geo-coordinate and contact details
# ##############################################################################
class LinkedLocationCheck(LinkedCheck):
    is_camp_location = models.BooleanField(default=False)
    center_latitude = models.FloatField(
        null=True, blank=True, default=50.4956754)
    center_longitude = models.FloatField(
        null=True, blank=True, default=3.3452037)
    zoom = DefaultIntegerField(default=7)

    locations = models.ManyToManyField(LinkedLocation, related_name="checks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_value(self) -> bool:
        if self.locations and self.locations.count() > 0:
            return True
        return False


# ##############################################################################
# LinkedParticipantCheck
#
# A check that selects members and non-members
# ##############################################################################
class LinkedParticipantCheck(LinkedCheck):
    participant_check_type = DefaultCharField(
        choices=ParticipantType.choices,
        default=ParticipantType.PARTICIPANT,
        max_length=1,
    )
    participants = models.ManyToManyField(
        VisumParticipant, related_name="checks")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.participant_check_type = kwargs.get(
            "participant_check_type", ParticipantType.PARTICIPANT
        )

    def first(self) -> VisumParticipant:
        if self.participants.count() == 0:
            return None
        return self.participants.first()

    def has_value(self) -> bool:
        return self.participants and self.participants.count() > 0


# ##############################################################################
# LinkedFileUploadCheck
#
# A check that contains a file
# ##############################################################################
class LinkedFileUploadCheck(LinkedCheck):
    value = models.ManyToManyField(PersistedFile, related_name="checks")

    def has_value(self) -> bool:
        if self.value:
            return True
        return False


# ##############################################################################
# LinkedCommentCheck
#
# A check that contains comments
# ##############################################################################
class LinkedCommentCheck(LinkedCheck):
    value = OptionalCharField(max_length=300)

    def has_value(self) -> bool:
        if self.value and CheckValidator.validate(self.parent.validators, self.value):
            return True
        return False


# ##############################################################################
# LinkedNumberCheck
#
# A check that contains numbers
# ##############################################################################
class LinkedNumberCheck(LinkedCheck):
    value = OptionalIntegerField()

    def has_value(self) -> bool:
        return CheckValidator.validate(self.parent.validators, self.value)
