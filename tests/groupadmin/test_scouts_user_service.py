"""
Tests for ScoutsUserService — specifically process_groups() and process_functions().

These tests lock in behaviour before the Pydantic migration. They do not hit
the database or the GA API; GroupAdminSettings calls are patched where needed.
"""
import pytest

from scouts_auth.groupadmin.models import (
    GaGroup,
    GaMemberFunction,
    GaFunctionDescription,
    GaGrouping,
    ScoutsGroup,
    ScoutsRole,
)
from scouts_auth.groupadmin.serializers.value_objects import (
    GaGroupSerializer,
    GaMemberFunctionSerializer,
    GaFunctionDescriptionSerializer,
)
from scouts_auth.scouts.services.scouts_user_service import ScoutsUserService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_ga_group(group_admin_id: str, name: str = "Test Scouts", child_groups=None) -> GaGroup:
    data = {"id": group_admin_id, "naam": name, "soort": "groep", "links": []}
    if child_groups:
        data["onderliggendeGroepen"] = child_groups
    s = GaGroupSerializer()
    return s.create(s.to_internal_value(data))


def _make_ga_member_function(function_id: str, group_admin_id: str, code: str = "GVL", end: str = None) -> GaMemberFunction:
    data = {
        "groep": group_admin_id,
        "functie": function_id,
        "begin": "2023-09-01T00:00:00",
        "code": code,
        "omschrijving": "Test functie",
        "links": [],
    }
    if end:
        data["einde"] = end
    s = GaMemberFunctionSerializer()
    return s.create(s.to_internal_value(data))


def _make_ga_function_description(function_id: str, code: str, grouping_name: str = "Leden") -> GaFunctionDescription:
    data = {
        "id": function_id,
        "type": "sectie",
        "code": code,
        "omschrijving": "Test functie beschrijving",
        "groeperingen": [{"naam": grouping_name, "volgorde": 1}],
        "groepen": [],
        "links": [],
    }
    s = GaFunctionDescriptionSerializer()
    return s.create(s.to_internal_value(data))


# ---------------------------------------------------------------------------
# process_groups
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_process_groups_returns_scouts_group():
    abstract_groups = [_make_ga_group("A1234B", "Test Scouts")]
    service = ScoutsUserService()
    result = service.process_groups(abstract_groups=abstract_groups)
    assert len(result) == 1
    assert isinstance(result[0], ScoutsGroup)
    assert result[0].group_admin_id == "A1234B"
    assert result[0].name == "Test Scouts"


@pytest.mark.unit
def test_process_groups_multiple_groups():
    abstract_groups = [
        _make_ga_group("A1234B"),
        _make_ga_group("A1234G"),
    ]
    service = ScoutsUserService()
    result = service.process_groups(abstract_groups=abstract_groups)
    assert len(result) == 2
    ids = {g.group_admin_id for g in result}
    assert ids == {"A1234B", "A1234G"}


@pytest.mark.unit
def test_process_groups_detects_child_groups():
    abstract_groups = [
        _make_ga_group("A1234", child_groups=["A1234B", "A1234G"]),
        _make_ga_group("A1234B"),
        _make_ga_group("A1234G"),
    ]
    service = ScoutsUserService()
    result = service.process_groups(abstract_groups=abstract_groups)
    parent = next(g for g in result if g.group_admin_id == "A1234")
    assert parent.has_child_groups()
    assert "A1234B" in parent.get_child_groups()
    assert "A1234G" in parent.get_child_groups()


# ---------------------------------------------------------------------------
# process_functions
# ---------------------------------------------------------------------------

class _MockUser:
    username = "jan.janssen"


class _MockMember:
    def __init__(self, functions):
        self.functions = functions


@pytest.mark.unit
def test_process_functions_includes_leader(mocker):
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_inactive_functions_in_profile",
        return_value=True,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_only_leader_functions_in_profile",
        return_value=False,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.get_leadership_status_identifier",
        return_value="Leiding",
    )

    group = _make_ga_group("A1234B")
    scouts_group = ScoutsGroup.from_abstract_scouts_group(abstract_group=group)
    fn = _make_ga_member_function("abc-123", "A1234B", "GVL")
    desc = _make_ga_function_description("abc-123", "GVL", grouping_name="Leiding")

    service = ScoutsUserService()
    result = service.process_functions(
        active_user=_MockUser(),
        user_groups=[scouts_group],
        abstract_member=_MockMember(functions=[fn]),
        abstract_function_descriptions=[desc],
    )

    assert len(result) == 1
    assert isinstance(result[0], ScoutsRole)
    assert result[0].is_leader is True
    assert result[0].code == "GVL"


@pytest.mark.unit
def test_process_functions_excludes_inactive_when_configured(mocker):
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_inactive_functions_in_profile",
        return_value=False,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_only_leader_functions_in_profile",
        return_value=False,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.get_leadership_status_identifier",
        return_value="Leiding",
    )

    group = _make_ga_group("A1234B")
    scouts_group = ScoutsGroup.from_abstract_scouts_group(abstract_group=group)
    fn_inactive = _make_ga_member_function("abc-123", "A1234B", end="2022-06-30T00:00:00")
    fn_active = _make_ga_member_function("def-456", "A1234B", code="LID")
    desc_inactive = _make_ga_function_description("abc-123", "GVL")
    desc_active = _make_ga_function_description("def-456", "LID")

    service = ScoutsUserService()
    result = service.process_functions(
        active_user=_MockUser(),
        user_groups=[scouts_group],
        abstract_member=_MockMember(functions=[fn_inactive, fn_active]),
        abstract_function_descriptions=[desc_inactive, desc_active],
    )

    assert len(result) == 1
    assert result[0].code == "LID"


@pytest.mark.unit
def test_process_functions_non_leader_excluded_when_only_leaders_required(mocker):
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_inactive_functions_in_profile",
        return_value=True,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.include_only_leader_functions_in_profile",
        return_value=True,
    )
    mocker.patch(
        "scouts_auth.scouts.services.scouts_user_service.GroupAdminSettings.get_leadership_status_identifier",
        return_value="Leiding",
    )

    group = _make_ga_group("A1234B")
    scouts_group = ScoutsGroup.from_abstract_scouts_group(abstract_group=group)
    fn = _make_ga_member_function("abc-123", "A1234B", code="LID")
    desc = _make_ga_function_description("abc-123", "LID", grouping_name="Leden")

    service = ScoutsUserService()
    result = service.process_functions(
        active_user=_MockUser(),
        user_groups=[scouts_group],
        abstract_member=_MockMember(functions=[fn]),
        abstract_function_descriptions=[desc],
    )

    assert len(result) == 0
