from typing import Dict
from uuid import UUID

from django.db import transaction

from apps.camps.models import CampYear
from apps.camps.services import CampYearService

from apps.visums.models import Category, SubCategory, Check

from apps.deadlines.models import Deadline, DeadlineItem
from apps.deadlines.services import DeadlineService


import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampYearCloneService:
    """
    Clones the previous camp year's categories, sub-categories, checks and deadlines
    into the current camp year, so a new camp year no longer needs to be built up by
    hand editing fixture JSON.
    """

    deadline_service = DeadlineService()

    def clone_to_current_year(self) -> tuple[str, bool]:
        """
        Returns a tuple of (message, cloned). cloned is False for the two "nothing to
        do" cases (target year already has content, or there is no previous year to
        clone from), so callers can distinguish a warning from an actual result.
        """
        target_year: CampYear = CampYearService().get_or_create_current_camp_year()

        if Category.objects.filter(camp_year=target_year).exists():
            return (
                f"Werkjaar {target_year.year} heeft al categorieën, er is niets gedaan.",
                False,
            )

        source_year: CampYear = CampYear.objects.safe_get(year=target_year.year - 1)
        if not source_year or not Category.objects.filter(camp_year=source_year).exists():
            return (
                f"Werkjaar {target_year.year - 1} heeft geen categorieën om van te klonen, "
                "er is niets gedaan.",
                False,
            )

        self._clone(source_year=source_year, target_year=target_year)

        return (f"Werkjaar {source_year.year} gekloond naar {target_year.year}.", True)

    @transaction.atomic
    def _clone(self, source_year: CampYear, target_year: CampYear) -> None:
        category_map: Dict[UUID, Category] = {}
        for category in Category.objects.filter(camp_year=source_year):
            camp_types = list(category.camp_types.all())

            new_category = Category(
                name=category.name,
                camp_year=target_year,
                priority=category.priority,
                index=category.index,
                label=category.label,
                description=category.description,
                explanation=category.explanation,
            )
            new_category.full_clean()
            new_category.save()
            new_category.camp_types.set(camp_types)

            category_map[category.id] = new_category

        sub_category_map: Dict[UUID, SubCategory] = {}
        for sub_category in SubCategory.objects.filter(category_id__in=category_map.keys()):
            camp_types = list(sub_category.camp_types.all())

            new_sub_category = SubCategory(
                name=sub_category.name,
                category=category_map[sub_category.category_id],
                index=sub_category.index,
                label=sub_category.label,
                description=sub_category.description,
                explanation=sub_category.explanation,
                link=sub_category.link,
            )
            new_sub_category.full_clean()
            new_sub_category.save()
            new_sub_category.camp_types.set(camp_types)

            sub_category_map[sub_category.id] = new_sub_category

        check_map: Dict[UUID, Check] = {}
        for check in Check.objects.filter(sub_category_id__in=sub_category_map.keys()):
            camp_types = list(check.camp_types.all())

            new_check = Check(
                name=check.name,
                sub_category=sub_category_map[check.sub_category_id],
                check_type=check.check_type,
                index=check.index,
                is_multiple=check.is_multiple,
                is_member=check.is_member,
                is_required_for_validation=check.is_required_for_validation,
                requires_permission=check.requires_permission,
                linked_to=check.linked_to,
                change_handlers=check.change_handlers,
                validators=check.validators,
                label=check.label,
                explanation=check.explanation,
                link=check.link,
            )
            new_check.full_clean()
            new_check.save()
            new_check.camp_types.set(camp_types)

            check_map[check.id] = new_check

        for deadline in Deadline.objects.filter(camp_year=source_year):
            camp_types = list(deadline.camp_types.all())

            new_deadline = Deadline(
                name=deadline.name,
                camp_year=target_year,
                is_important=deadline.is_important,
                is_camp_registration=deadline.is_camp_registration,
                index=deadline.index,
                label=deadline.label,
                description=deadline.description,
                explanation=deadline.explanation,
            )
            new_deadline.full_clean()
            new_deadline.save()
            new_deadline.camp_types.set(camp_types)

            # Same day and month as the source year, the year itself moves to the
            # target year. calculated_date is recomputed by the service, not copied.
            old_due_date = deadline.due_date
            self.deadline_service.create_deadline_date(
                deadline=new_deadline,
                date_day=old_due_date.date_day,
                date_month=old_due_date.date_month,
                date_year=target_year.year,
            )

            for item in deadline.items.all():
                new_item = DeadlineItem(
                    deadline=new_deadline,
                    deadline_item_type=item.deadline_item_type,
                    index=item.index,
                    item_flag=item.item_flag,
                    item_sub_category=(
                        sub_category_map.get(item.item_sub_category_id)
                        if item.item_sub_category_id
                        else None
                    ),
                    item_check=(check_map.get(item.item_check_id) if item.item_check_id else None),
                )
                new_item.full_clean()
                new_item.save()
