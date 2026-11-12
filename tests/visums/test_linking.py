from types import SimpleNamespace

import pytest

from apps.visums.models import CampVisum, LinkedCheck
from apps.visums.services import LinkedCategorySetService


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


@pytest.mark.django_db
def test_check_with_two_camp_types_is_linked_once(template_year):
    from apps.camps.models import CampType

    second_type = CampType.objects.exclude(pk=template_year.camp_type.pk).first()
    template_year.check.camp_types.add(second_type)
    visum = CampVisum.objects.create(year=template_year.camp_year, name="Kamp", group="X1234G", group_name="Groep")
    visum.camp_types.set([template_year.camp_type, second_type])

    LinkedCategorySetService().create_linked_category_set(request=REQUEST, visum=visum)

    assert linked_check_names(visum) == ["check"]
