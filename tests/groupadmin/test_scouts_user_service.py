"""
Tests for ScoutsUserService: building the user from the groups in groepsadmin.

These tests don't hit the database or the GA API.
"""
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from scouts_auth.groupadmin.models import GaGroup, ScoutsGroup
from scouts_auth.groupadmin.serializers.value_objects import GaGroupSerializer
from scouts_auth.scouts.services.scouts_user_service import ScoutsUserService


def _make_ga_group(number: str, name: str = "Test Scouts", responsibilities=None) -> GaGroup:
    # GA returns an internal id as "id" in rest-ga/groep, the groepsnummer comes separately
    data = {"id": f"oid-{number.lower()}", "groepsnummer": number, "naam": name, "soort": "groep", "links": []}
    if responsibilities is not None:
        data["verantwoordelijkheden"] = responsibilities
    s = GaGroupSerializer()
    return s.create(s.to_internal_value(data))


@pytest.mark.unit
def test_process_groups_returns_scouts_group():
    abstract_groups = [_make_ga_group("A1234B", "Test Scouts")]
    result = ScoutsUserService().process_groups(abstract_groups=abstract_groups)
    assert len(result) == 1
    assert isinstance(result[0], ScoutsGroup)
    assert result[0].number == "A1234B"
    assert result[0].name == "Test Scouts"


@pytest.mark.unit
def test_process_groups_multiple_groups():
    abstract_groups = [_make_ga_group("A1234B"), _make_ga_group("A1234G")]
    result = ScoutsUserService().process_groups(abstract_groups=abstract_groups)
    assert {g.number for g in result} == {"A1234B", "A1234G"}


@pytest.mark.unit
def test_process_groups_copies_responsibilities():
    abstract_groups = [_make_ga_group("X1201G", responsibilities=["leiding", "algemeen"]), _make_ga_group("X1202M")]
    result = {g.number: g for g in ScoutsUserService().process_groups(abstract_groups=abstract_groups)}
    assert result["X1201G"].responsibilities == ["leiding", "algemeen"]
    assert result["X1202M"].responsibilities == []


@pytest.mark.unit
def test_get_scouts_user_does_not_call_the_function_endpoint(mocker):
    """auth/me is built from the responsibilities in rest-ga/groep, without calling rest-ga/functie."""
    service = ScoutsUserService()
    groupadmin = MagicMock()
    groupadmin.get_groups.return_value = SimpleNamespace(
        scouts_groups=[_make_ga_group("X1201G", responsibilities=["leiding"])]
    )
    mocker.patch.object(service, "groupadmin", groupadmin)
    mocker.patch.object(service, "permission_service", MagicMock())
    mocker.patch.object(service, "section_service", MagicMock())
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.ScoutsUser.has_administrator_groups", return_value=False
    )
    active_user = MagicMock()

    service.get_scouts_user(active_user=active_user, abstract_member=MagicMock())

    groupadmin.get_function_descriptions.assert_not_called()
    added = [call.kwargs["scouts_group"] for call in active_user.add_scouts_group.call_args_list]
    assert [(g.number, g.responsibilities) for g in added] == [("X1201G", ["leiding"])]
