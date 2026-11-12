from types import SimpleNamespace

import pytest

from apps.visums.models import CampVisum, LinkedCheck
from apps.visums.services import LinkedCategorySetService, LinkedCategoryService

from tests.conftest import add_check

REQUEST = SimpleNamespace(user=None)


def create_visum(template_year) -> CampVisum:
    visum = CampVisum.objects.create(year=template_year.camp_year, name="Kamp", group="X1234G", group_name="Groep")
    visum.camp_types.set([template_year.camp_type])
    LinkedCategorySetService().create_linked_category_set(request=REQUEST, visum=visum)
    return visum


def linked_check_names(visum: CampVisum) -> list:
    return sorted(
        LinkedCheck.objects.filter(sub_category__category__category_set__visum=visum, is_archived=False).values_list(
            "parent__name", flat=True
        )
    )


def update(visum: CampVisum) -> None:
    LinkedCategoryService().update_linked_categories(request=REQUEST, linked_category_set=visum.category_set)


@pytest.mark.django_db
def test_new_visum_skips_an_archived_check(template_year):
    add_check(template_year.sub_category, "archived", [template_year.camp_type])
    template_year.sub_category.checks.filter(name="archived").update(is_archived=True)

    assert linked_check_names(create_visum(template_year)) == ["check"]


@pytest.mark.django_db
def test_existing_visum_keeps_a_check_archived_later(template_year):
    visum = create_visum(template_year)
    template_year.sub_category.checks.filter(name="check").update(is_archived=True)

    update(visum)

    assert linked_check_names(visum) == ["check"]


@pytest.mark.django_db
def test_existing_visum_does_not_gain_an_archived_check(template_year):
    visum = create_visum(template_year)
    add_check(template_year.sub_category, "archived", [template_year.camp_type])
    template_year.sub_category.checks.filter(name="archived").update(is_archived=True)

    update(visum)

    assert linked_check_names(visum) == ["check"]


@pytest.mark.django_db
def test_check_with_two_camp_types_is_linked_once(template_year):
    from apps.camps.models import CampType

    second_type = CampType.objects.exclude(pk=template_year.camp_type.pk).first()
    template_year.check.camp_types.add(second_type)
    visum = CampVisum.objects.create(year=template_year.camp_year, name="Kamp", group="X1234G", group_name="Groep")
    visum.camp_types.set([template_year.camp_type, second_type])

    LinkedCategorySetService().create_linked_category_set(request=REQUEST, visum=visum)

    assert linked_check_names(visum) == ["check"]
