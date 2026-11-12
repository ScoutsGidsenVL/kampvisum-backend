from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from django.utils import timezone

from apps.visums.models import Category, SubCategory, Check
from apps.deadlines.models import DeadlineItem


class TemplateArchiveService:
    """
    Archives and restores template categories, sub-categories and checks. A new visum skips
    an archived item, so an item a deadline points at cannot be archived: linking that
    deadline to a new visum would fail on the missing linked item.
    """

    DEADLINE_ITEM_LOOKUPS = {
        Category: ("item_sub_category__category__in", "item_check__sub_category__category__in"),
        SubCategory: ("item_sub_category__in", "item_check__sub_category__in"),
        Check: ("item_check__in",),
    }

    def archive(self, queryset: QuerySet, user) -> None:
        query = Q()
        for lookup in self.DEADLINE_ITEM_LOOKUPS[queryset.model]:
            query |= Q(**{lookup: queryset})

        deadline_labels = sorted(set(DeadlineItem.objects.filter(query).values_list("deadline__label", flat=True)))
        if deadline_labels:
            raise ValidationError(
                "Niets gearchiveerd: deadline %(deadlines)s verwijst naar een geselecteerd item.",
                params={"deadlines": ", ".join(f"„{label}”" for label in deadline_labels)},
            )

        queryset.update(is_archived=True, archived_by=user, archived_on=timezone.now())

    def restore(self, queryset: QuerySet) -> None:
        queryset.update(is_archived=False, archived_by=None, archived_on=timezone.now())
