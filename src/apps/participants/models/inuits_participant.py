from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.participants.managers import InuitsParticipantManager

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.models.fields import OptionalGroupAdminIdField

from scouts_auth.inuits.models import InuitsPerson, Gender, GenderHelper
from scouts_auth.inuits.models.fields import OptionalCharField


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class InuitsParticipant(InuitsPerson):
    objects = InuitsParticipantManager()

    group_group_admin_id = OptionalGroupAdminIdField(null=True)
    group_admin_id = OptionalGroupAdminIdField(null=True)
    is_member = models.BooleanField(default=False)
    comment = OptionalCharField(max_length=300)
    inactive_member = models.BooleanField(default=False)

    class Meta:
        ordering = ["first_name", "last_name", "birth_date", "group_group_admin_id"]
        constraints = [
            models.UniqueConstraint(
                fields=["group_group_admin_id", "email"],
                name="unique_group_and_email_if_email_present",
                condition=Q(email__isnull=False) & ~Q(email__exact=""),
            ),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has_group_admin_id(self) -> bool:
        return hasattr(self, "group_admin_id") and self.group_admin_id

    def exists(self) -> bool:
        return InuitsParticipant.objects.exists(self.id)

    def equals_participant(self, updated_participant):
        if updated_participant is None:
            return False

        if (
            not isinstance(updated_participant, InuitsParticipant)
            or not type(updated_participant).__class__.__name__ == self.__class__.__name__
            and type(updated_participant).__class__.__name__ != "ModelBase"
        ):
            # logger.debug(
            #     type(updated_participant).__class__.__name__,
            #     self.__class__.__name__,
            # )
            return False

        return (
            self.equals_person(updated_participant)
            and self.group_group_admin_id == updated_participant.group_group_admin_id
            and self.group_admin_id == updated_participant.group_group_admin_id
            and self.is_member == updated_participant.is_member
            and self.comment == updated_participant.comment
            and self.inactive_member == updated_participant.inactive_member
            and self.participant_type == updated_participant.participant_type
        )

    def __str__(self):
        return "id ({}), is_member ({}), group_group_admin_id ({}), group_admin_id ({}), {}, comment ({}), inactive_member ({})".format(
            self.id,
            self.is_member,
            self.group_group_admin_id,
            self.group_admin_id,
            self.person_to_str(),
            self.comment,
            self.inactive_member,
        )

    @staticmethod
    def from_scouts_member(scouts_member: AbstractScoutsMember, instance=None):
        if not scouts_member:
            raise ValidationError("AbstractScoutsMember not initialized")
        if not scouts_member.group_admin_id:
            raise ValidationError("Can't create an InuitsParticipant without a valid group admin id")
        participant = instance
        if not participant:
            participant = InuitsParticipant()

        participant.id = scouts_member.group_admin_id
        participant.group_admin_id = scouts_member.group_admin_id
        participant.is_member = True
        participant.first_name = scouts_member.first_name if scouts_member.first_name else ""
        participant.last_name = scouts_member.last_name if scouts_member.last_name else ""
        participant.phone_number = scouts_member.phone_number if scouts_member.phone_number else ""
        participant.email = scouts_member.email if scouts_member.email else ""
        participant.birth_date = scouts_member.birth_date if scouts_member.birth_date else None
        # cell_number, letter_box, gender and address fields are absent on search results (AbstractScoutsMemberSearchMember)
        participant.cell_number = getattr(scouts_member, "cell_number", "")
        participant.gender = getattr(scouts_member, "gender", Gender.UNKNOWN)
        participant.street = getattr(scouts_member, "street", "")
        participant.number = getattr(scouts_member, "number", "")
        participant.letter_box = getattr(scouts_member, "letter_box", "")
        participant.postal_code = getattr(scouts_member, "postal_code", "")
        participant.city = getattr(scouts_member, "city", "")
        participant.group_group_admin_id = ""
        participant.comment = ""
        participant.inactive_member = scouts_member.inactive_member

        return participant
