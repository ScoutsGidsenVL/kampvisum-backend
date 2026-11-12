import datetime

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command

from apps.camps.models import CampType, CampYear
from apps.camps.services import CampYearCloneService, CampYearService
from apps.camps.services.camp_year_clone_service import COPIED_FIELDS
from apps.deadlines.models import Deadline, DeadlineDate, DeadlineItem
from apps.deadlines.models.enums import DeadlineItemType
from apps.visums.models import Category, CategoryPriority, Check, SubCategory
from scouts_auth.groupadmin.models import ScoutsUser

from tests.conftest import add_check

ARCHIVE_FIELDS = {"is_archived", "archived_by", "archived_on"}
SET_BY_CLONE = {
    Category: {"id", "camp_year", "camp_types"} | ARCHIVE_FIELDS,
    SubCategory: {"id", "category", "camp_types"} | ARCHIVE_FIELDS,
    Check: {"id", "sub_category", "camp_types"} | ARCHIVE_FIELDS,
    Deadline: {"id", "camp_year", "camp_types", "created_by", "created_on", "updated_by", "updated_on"},
    DeadlineItem: {"id", "deadline", "item_sub_category", "item_check"},
    DeadlineDate: {"id", "deadline", "date_day", "date_month", "date_year", "calculated_date"},
}


@pytest.fixture
def source(past_camp_year):
    """Last year's template: active and archived rows, and a deadline per date case."""
    call_command("loaddata", "camp_types", "category_priorities", "check_types", verbosity=0)
    camp_type = CampType.objects.get(camp_type="basis")

    category = Category.objects.create(
        name="category", camp_year=past_camp_year, priority=CategoryPriority.objects.first(), label="Categorie"
    )
    category.camp_types.set([camp_type])
    sub_category = SubCategory.objects.create(name="sub_category", category=category, label="Subcategorie")
    sub_category.camp_types.set([camp_type])
    archived_sub_category = SubCategory.objects.create(name="archived_sub", category=category, is_archived=True)
    add_check(archived_sub_category, "under_archived_sub", [camp_type])
    check = add_check(sub_category, "check", [camp_type])
    archived_check = add_check(sub_category, "archived_check", [camp_type])
    archived_check.is_archived = True
    archived_check.save()

    def deadline(name, date=None):
        row = Deadline.objects.create(name=name, camp_year=past_camp_year, label=name)
        row.camp_types.set([camp_type])
        if date:
            day, month, year = date
            DeadlineDate.objects.create(
                deadline=row,
                date_day=day,
                date_month=month,
                date_year=year,
                calculated_date=datetime.date(year or past_camp_year.end_date.year, month, day),
            )
        return row

    autumn = deadline("autumn", (15, 10, past_camp_year.start_date.year))
    DeadlineItem.objects.create(deadline=autumn, deadline_item_type=DeadlineItemType.LINKED_CHECK, item_check=check)
    DeadlineItem.objects.create(
        deadline=autumn, deadline_item_type=DeadlineItemType.LINKED_CHECK, item_check=archived_check
    )
    deadline("no_year", (31, 3, None))
    deadline("no_date")
    deadline("leap_day", (29, 2, 2024))

    return past_camp_year


@pytest.fixture
def target(source):
    return CampYearService().get_or_create_current_camp_year()


def names(model, **filters):
    return sorted(model.objects.filter(**filters).values_list("name", flat=True))


def due_date(target_year, name):
    return DeadlineDate.objects.get(deadline__camp_year=target_year, deadline__name=name)


@pytest.mark.parametrize("model", list(SET_BY_CLONE), ids=lambda model: model.__name__)
def test_every_field_is_copied_or_set_by_the_clone(model):
    fields = {field.name for field in model._meta.get_fields() if field.concrete}

    assert fields == set(COPIED_FIELDS.get(model, ())) | SET_BY_CLONE[model]


@pytest.mark.django_db
def test_clone_skips_archived_rows(source, target):
    user = ScoutsUser.objects.create_user(username="beheerder", email="beheerder@example.invalid")

    CampYearCloneService().clone_year(source, target, user)

    assert names(Category, camp_year=target) == ["category"]
    assert names(SubCategory, category__camp_year=target) == ["sub_category"]
    assert names(Check, sub_category__category__camp_year=target) == ["check"]
    assert names(Deadline, camp_year=target) == ["autumn", "leap_day", "no_date", "no_year"]
    assert Check.objects.get(sub_category__category__camp_year=target).camp_types.get().camp_type == "basis"
    assert set(Deadline.objects.filter(camp_year=target).values_list("created_by", flat=True)) == {user.id}


@pytest.mark.django_db
def test_clone_skips_a_deadline_item_on_an_archived_check(source, target):
    CampYearCloneService().clone_year(source, target)

    item = DeadlineItem.objects.get(deadline__camp_year=target)
    assert item.item_check == Check.objects.get(sub_category__category__camp_year=target, name="check")


@pytest.mark.django_db
def test_clone_moves_a_fixed_year_and_keeps_a_date_without_year(source, target):
    CampYearCloneService().clone_year(source, target)

    autumn = due_date(target, "autumn")
    assert (autumn.date_day, autumn.date_month, autumn.date_year) == (15, 10, target.start_date.year)
    no_year = due_date(target, "no_year")
    assert no_year.date_year is None
    assert no_year.calculated_date == datetime.date(target.end_date.year, 3, 31)


@pytest.mark.django_db
def test_clone_survives_a_missing_date_and_a_leap_day(source, target):
    CampYearCloneService().clone_year(source, target)

    assert not DeadlineDate.objects.filter(deadline__camp_year=target, deadline__name="no_date").exists()
    leap_day = due_date(target, "leap_day")
    assert (leap_day.date_day, leap_day.date_month, leap_day.date_year) == (28, 2, 2025)


@pytest.mark.django_db
def test_clone_twice_creates_nothing_the_second_time(source, target):
    service = CampYearCloneService()
    first = service.clone_year(source, target)

    assert first == 1 + 1 + 1 + 4 + 3 + 1  # category, sub-category, check, deadlines, dates, item
    assert service.clone_year(source, target) == 0
    assert names(Check, sub_category__category__camp_year=target) == ["check"]


@pytest.mark.django_db
def test_clone_completes_a_year_with_deadlines_but_no_categories(source, target):
    Deadline.objects.create(name="autumn", camp_year=target, label="autumn")

    CampYearCloneService().clone_year(source, target)

    assert names(Category, camp_year=target) == ["category"]
    assert names(Deadline, camp_year=target) == ["autumn", "leap_day", "no_date", "no_year"]
    assert DeadlineItem.objects.filter(deadline__camp_year=target).count() == 1


@pytest.mark.django_db
def test_clone_refuses_and_names_every_deadline_left_without_items(source, target):
    DeadlineItem.objects.filter(deadline__name="autumn", item_check__name="check").delete()
    archived_check = Check.objects.get(sub_category__category__camp_year=source, name="archived_check")
    DeadlineItem.objects.create(
        deadline=Deadline.objects.get(camp_year=source, name="no_year"),
        deadline_item_type=DeadlineItemType.LINKED_CHECK,
        item_check=archived_check,
    )

    with pytest.raises(ValidationError, match="„autumn”, „no_year”"):
        CampYearCloneService().clone_year(source, target)

    assert not Category.objects.filter(camp_year=target).exists()
    assert not Deadline.objects.filter(camp_year=target).exists()


@pytest.mark.django_db
def test_failed_clone_leaves_no_camp_year_behind(source, mocker):
    current_year = CampYearService().get_current_camp_year()
    assert current_year is None
    mocker.patch.object(CampYearCloneService, "clone_year", side_effect=RuntimeError)

    with pytest.raises(RuntimeError):
        CampYearCloneService().clone_to_current_year()

    assert CampYear.objects.filter(year=source.year + 1).count() == 0
