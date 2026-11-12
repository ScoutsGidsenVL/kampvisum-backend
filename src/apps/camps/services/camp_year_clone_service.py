import calendar
import datetime
from typing import Dict
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.camps.models import CampYear
from apps.camps.services import CampYearService

from apps.visums.models import Category, SubCategory, Check

from apps.deadlines.models import Deadline, DeadlineDate, DeadlineItem


import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


# The fields copied as-is. The parent, the camp types and the date are set by the clone itself;
# tests/camps/test_camp_year_clone.py fails when a model gains a field that is in neither list.
COPIED_FIELDS = {
    Category: ("name", "priority", "index", "label", "description", "explanation"),
    SubCategory: ("name", "index", "label", "description", "explanation", "link"),
    Check: (
        "name",
        "check_type",
        "index",
        "is_multiple",
        "is_member",
        "is_required_for_validation",
        "requires_permission",
        "linked_to",
        "change_handlers",
        "validators",
        "label",
        "explanation",
        "link",
    ),
    Deadline: ("name", "is_important", "is_camp_registration", "index", "label", "description", "explanation"),
    DeadlineItem: ("deadline_item_type", "index", "item_flag"),
}


class CampYearCloneService:
    """
    Clones a camp year's categories, sub-categories, checks and deadlines into another camp year,
    so a new camp year no longer needs to be built up by hand editing fixture JSON.
    """

    @transaction.atomic
    def clone_to_current_year(self, user=None) -> tuple[str, bool]:
        """
        Clones the previous camp year into the current one. Returns (message, cloned); cloned is
        False when there was nothing to do, so callers can tell a warning from a result.
        """
        target_year: CampYear = CampYearService().get_or_create_current_camp_year()
        source_year: CampYear = CampYear.objects.safe_get(year=target_year.year - 1)
        if not source_year or not Category.objects.filter(camp_year=source_year).exists():
            return (
                f"Kampjaar {target_year.year - 1} heeft geen categorieën om van te klonen, er is niets gedaan.",
                False,
            )

        created = self.clone_year(source_year, target_year, user)
        if not created:
            return (
                f"Kampjaar {target_year.year} bevat al alles uit {source_year.year}, er is niets gedaan.",
                False,
            )
        return (f"Kampjaar {source_year.year} gekloond naar {target_year.year}: {created} onderdelen aangemaakt.", True)

    @transaction.atomic
    def clone_year(self, source: CampYear, target: CampYear, user=None) -> int:
        """
        Copies what the target year lacks and returns the number of rows created. A target row with
        the same name under the same parent counts as already cloned, so a half-finished clone can be
        completed. Archived rows are not cloned. Raises ValidationError, and keeps nothing, when a
        deadline would lose all its items: a deadline without items breaks every new visum.
        """
        self.created = 0
        years = {source.id: target}

        categories = self._clone_rows(
            Category.objects.filter(camp_year=source, is_archived=False),
            Category.objects.filter(camp_year=target),
            "camp_year",
            years,
        )
        sub_categories = self._clone_rows(
            SubCategory.objects.filter(category_id__in=categories, is_archived=False),
            SubCategory.objects.filter(category__camp_year=target),
            "category",
            categories,
        )
        checks = self._clone_rows(
            Check.objects.filter(sub_category_id__in=sub_categories, is_archived=False),
            Check.objects.filter(sub_category__category__camp_year=target),
            "sub_category",
            sub_categories,
        )
        deadlines = self._clone_rows(
            Deadline.objects.filter(camp_year=source),
            Deadline.objects.filter(camp_year=target),
            "camp_year",
            years,
            created_by=user,
        )

        left_without_items = []
        for deadline in Deadline.objects.filter(camp_year=source).prefetch_related("items"):
            clone = deadlines[deadline.id]
            source_date = DeadlineDate.objects.filter(deadline=deadline).first()
            if source_date and not DeadlineDate.objects.filter(deadline=clone).exists():
                self._clone_date(source_date, clone, target, year_shift=target.year - source.year)
            self._clone_items(deadline, clone, sub_categories, checks)
            if deadline.items.all() and not clone.items.exists():
                left_without_items.append(deadline.label or deadline.name)

        if left_without_items:
            raise ValidationError(
                "Niets gekloond: deadline %(deadlines)s verwijst enkel naar gearchiveerde items.",
                params={"deadlines": ", ".join(f"„{label}”" for label in left_without_items)},
            )
        return self.created

    def _clone_rows(
        self, sources, existing, parent_field: str, parents: Dict[UUID, models.Model], **overrides
    ) -> Dict[UUID, models.Model]:
        """
        Maps each source row id to its copy under the cloned parent, reusing a same-named target row.
        All four models are unique by name within their parent.
        """
        existing_by_name = {(getattr(row, f"{parent_field}_id"), row.name): row for row in existing}

        clones = {}
        for row in sources:
            parent = parents[getattr(row, f"{parent_field}_id")]
            clone = existing_by_name.get((parent.id, row.name))
            if clone is None:
                clone = self._copy(row, **{parent_field: parent}, **overrides)
                clone.camp_types.set(row.camp_types.all())
            clones[row.id] = clone
        return clones

    def _clone_items(self, deadline: Deadline, clone: Deadline, sub_categories, checks) -> None:
        existing = {
            (item.deadline_item_type, item.item_flag_id, item.item_sub_category_id, item.item_check_id)
            for item in clone.items.all()
        }
        for item in deadline.items.all():
            sub_category = sub_categories.get(item.item_sub_category_id)
            check = checks.get(item.item_check_id)
            # The item points at a row that was not cloned, an archived one.
            if (item.item_sub_category_id and not sub_category) or (item.item_check_id and not check):
                continue
            key = (
                item.deadline_item_type,
                item.item_flag_id,
                getattr(sub_category, "id", None),
                getattr(check, "id", None),
            )
            if key not in existing:
                self._copy(item, deadline=clone, item_sub_category=sub_category, item_check=check)

    def _clone_date(self, source_date: DeadlineDate, deadline: Deadline, target: CampYear, year_shift: int) -> None:
        """A fixed year moves along with the camp year; a date without a year stays without one."""
        day, month = source_date.date_day, source_date.date_month
        year = source_date.date_year + year_shift if source_date.date_year else None
        calendar_year = year or (
            target.start_date.year if (month or 1) >= target.start_date.month else target.end_date.year
        )
        if month == 2 and day == 29 and not calendar.isleap(calendar_year):
            day = 28

        date = DeadlineDate(
            deadline=deadline,
            date_day=day,
            date_month=month,
            date_year=year,
            calculated_date=datetime.date(calendar_year, month or 1, day or 1),
        )
        date.full_clean()
        date.save()
        self.created += 1

    def _copy(self, source: models.Model, **overrides) -> models.Model:
        model = type(source)
        clone = model(**{field: getattr(source, field) for field in COPIED_FIELDS[model]}, **overrides)
        clone.full_clean()
        clone.save()
        self.created += 1
        return clone
