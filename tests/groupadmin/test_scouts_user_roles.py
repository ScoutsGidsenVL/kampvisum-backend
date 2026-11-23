"""
Tests for the roles of a ScoutsUser, derived from the responsibilities per group
(GA: verantwoordelijkheden). All groepsnummers are fictional.
"""
from typing import Dict, List

import pytest

from scouts_auth.groupadmin.models import ScoutsGroup, ScoutsUser


SECTION_LEADER = ScoutsUser.ROLE_SECTION_LEADER
GROUP_LEADER = ScoutsUser.ROLE_GROUP_LEADER
DISTRICT_COMMISSIONER = ScoutsUser.ROLE_DISTRICT_COMMISSIONER
REGIONAL = ScoutsUser.ROLE_REGIONAL


@pytest.fixture(autouse=True)
def no_admin_groups(settings):
    settings.KNOWN_ADMIN_GROUPS = []


def _user(groups: Dict[str, List[str]]) -> ScoutsUser:
    user = ScoutsUser(username="test.gebruiker")
    for number, responsibilities in groups.items():
        user.add_scouts_group(ScoutsGroup(number=number, name=number, responsibilities=responsibilities))
    return user


def _roles(user: ScoutsUser) -> Dict[str, List[str]]:
    return {number: sorted(user.get_roles_for_group(group_number=number)) for number in user.get_scouts_group_names()}


@pytest.mark.unit
def test_leader():
    user = _user({"X1201G": ["leiding"], "X1202M": []})
    assert _roles(user) == {"X1201G": [SECTION_LEADER], "X1202M": []}
    assert user.has_role_leader(group_number="X1201G")
    assert not user.has_role_leader(group_number="X1202M")


@pytest.mark.unit
def test_group_leader():
    user = _user({"X1201G": ["algemeen", "leiding"]})
    assert _roles(user) == {"X1201G": sorted([GROUP_LEADER, SECTION_LEADER])}


@pytest.mark.unit
def test_algemeen_on_district_or_gouw_is_no_group_leader():
    user = _user({"X1200D": ["algemeen"], "X1000P": ["algemeen"]})
    assert not user.has_role_group_leader(group_number="X1200D")
    assert not user.has_role_group_leader(group_number="X1000P")


@pytest.mark.unit
def test_district_commissioner():
    user = _user({"X1200D": ["algemeen"], "X1201G": ["regionaal"], "X1301G": ["regionaal"]})
    assert user.has_role_district_commissioner(group_number="X1200D")
    assert user.has_role_district_commissioner(group_number="X1201G")
    # Regional responsibility in another district, e.g. as a gouw adjunct
    assert not user.has_role_district_commissioner(group_number="X1301G")


@pytest.mark.unit
def test_district_commissioner_is_also_regional():
    user = _user({"X1200D": ["algemeen"], "X1201G": ["regionaal"]})
    assert _roles(user)["X1201G"] == sorted([DISTRICT_COMMISSIONER, REGIONAL])


@pytest.mark.unit
def test_regional():
    user = _user({"X1000P": ["algemeen"], "X1200D": ["regionaal"], "X1301S": ["regionaal"], "X1501K": ["regionaal"]})
    assert _roles(user) == {"X1000P": [], "X1200D": [REGIONAL], "X1301S": [REGIONAL], "X1501K": [REGIONAL]}
    assert [g.number for g in user.get_scouts_regional_groups()] == ["X1200D", "X1301S", "X1501K"]


@pytest.mark.unit
def test_gouw_is_no_district_commissioner():
    user = _user({"X1000P": ["algemeen"], "X1201G": ["regionaal"]})
    assert not user.has_role_district_commissioner(group_number="X1201G")
    assert user.has_role_regional(group_number="X1201G")


@pytest.mark.unit
def test_ignore_group():
    user = _user({"X1201G": ["regionaal"]})
    assert user.has_role_regional(ignore_group=True)
    assert not user.has_role_district_commissioner(ignore_group=True)
    assert not user.has_role_leader(ignore_group=True)


@pytest.mark.unit
def test_leader_groups_are_the_groups_with_a_role():
    user = _user({"X1201G": ["leiding"], "X1202M": [], "X1300D": ["regionaal"], "X1402G": ["evenementen"]})
    assert user.get_scouts_leader_group_names() == ["X1201G", "X1300D"]


@pytest.mark.unit
def test_unknown_group_has_no_roles():
    user = _user({"X1201G": ["leiding"]})
    assert user.get_roles_for_group(group_number="X9999G") == []
