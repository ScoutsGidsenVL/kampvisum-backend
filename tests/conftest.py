import datetime
from types import SimpleNamespace

import pytest
from django.core.management import call_command

from apps.camps.models import CampType
from apps.camps.services import CampYearService
from apps.visums.models import Category, CategoryPriority, CheckType, SubCategory, Check


@pytest.fixture
def template_year(db):
    """The current camp year with one category, sub-category and check, for the base camp type."""
    call_command("loaddata", "camp_types", "category_priorities", "check_types", verbosity=0)

    camp_year = CampYearService().get_or_create_current_camp_year()
    camp_type = CampType.objects.get(camp_type="basis")
    category = Category.objects.create(
        name="category", camp_year=camp_year, priority=CategoryPriority.objects.first(), label="Categorie"
    )
    category.camp_types.set([camp_type])
    sub_category = SubCategory.objects.create(name="sub_category", category=category, label="Subcategorie")
    sub_category.camp_types.set([camp_type])
    check = add_check(sub_category, "check", [camp_type])

    return SimpleNamespace(
        camp_year=camp_year, camp_type=camp_type, category=category, sub_category=sub_category, check=check
    )


def add_check(sub_category: SubCategory, name: str, camp_types) -> Check:
    check = Check.objects.create(
        name=name, sub_category=sub_category, check_type=CheckType.objects.get(check_type="SimpleCheck"), label=name
    )
    check.camp_types.set(camp_types)
    return check


@pytest.fixture
def past_camp_year(db):
    return CampYearService().get_or_create_year(None, date=datetime.date.today() - datetime.timedelta(days=365))
