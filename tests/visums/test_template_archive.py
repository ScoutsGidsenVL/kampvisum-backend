import pytest
from django.core.exceptions import ValidationError

from apps.deadlines.models import Deadline, DeadlineItem
from apps.deadlines.models.enums import DeadlineItemType
from apps.visums.models import Category, Check
from apps.visums.services import TemplateArchiveService


def point_deadline_at(check: Check) -> Deadline:
    deadline = Deadline.objects.create(
        name="deadline", camp_year=check.sub_category.category.camp_year, label="Kampmelding"
    )
    DeadlineItem.objects.create(deadline=deadline, deadline_item_type=DeadlineItemType.LINKED_CHECK, item_check=check)
    return deadline


@pytest.mark.django_db
def test_restore_sets_archived_on(template_year):
    checks = Check.objects.filter(pk=template_year.check.pk)
    TemplateArchiveService().archive(checks, user=None)

    TemplateArchiveService().restore(checks)

    check = checks.get()
    assert not check.is_archived
    assert check.archived_on is not None


@pytest.mark.django_db
def test_archive_refuses_a_check_a_deadline_points_at(template_year):
    point_deadline_at(template_year.check)

    with pytest.raises(ValidationError, match="Kampmelding"):
        TemplateArchiveService().archive(Check.objects.filter(pk=template_year.check.pk), user=None)

    template_year.check.refresh_from_db()
    assert not template_year.check.is_archived


@pytest.mark.django_db
def test_archive_refuses_a_category_with_a_check_a_deadline_points_at(template_year):
    point_deadline_at(template_year.check)

    with pytest.raises(ValidationError):
        TemplateArchiveService().archive(Category.objects.filter(pk=template_year.category.pk), user=None)
