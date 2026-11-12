import pytest

from apps.camps.services import CampYearService


@pytest.mark.django_db
def test_is_past(template_year, past_camp_year):
    assert CampYearService().is_past(past_camp_year)
    assert not CampYearService().is_past(template_year.camp_year)
