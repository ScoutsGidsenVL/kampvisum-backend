"""
Tests for ScoutsRole.is_active_function() and reading an old ScoutsUser session.
"""
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from scouts_auth.groupadmin.models import ScoutsRole
from scouts_auth.groupadmin.serializers import ScoutsUserSessionSerializer


def _role(end) -> ScoutsRole:
    role = ScoutsRole()
    role.end = end
    return role


@pytest.mark.unit
def test_function_without_end_date_is_active():
    assert _role(None).is_active_function() is True


@pytest.mark.unit
def test_function_with_end_date_is_inactive():
    assert _role(datetime(2020, 6, 30, tzinfo=timezone.utc)).is_active_function() is False


def _session(scouts_groups: list, scouts_functions: list) -> SimpleNamespace:
    # The session data is stored as a JSON string inside a JSON string
    data = json.dumps(json.dumps({"scouts_groups": scouts_groups, "scouts_functions": scouts_functions}, default=str))
    return SimpleNamespace(data=data)


@pytest.mark.unit
def test_old_session_without_number_falls_back_to_group_admin_id():
    session = _session(
        scouts_groups=[
            {"group_admin_id": "X9010G", "name": "Testgroep", "_child_group_names": "", "type": "Test"}
        ],
        scouts_functions=[],
    )

    group = ScoutsUserSessionSerializer.to_scouts_user(session)["scouts_groups"][0]

    assert group.number == "X9010G"
