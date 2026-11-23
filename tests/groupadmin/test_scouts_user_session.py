"""
Tests for storing the groups of a ScoutsUser in the session and reading them back.
"""
import json
from types import SimpleNamespace

import pytest

from scouts_auth.groupadmin.serializers import ScoutsUserSessionSerializer


def _session(data: dict) -> SimpleNamespace:
    # The session data is stored as a JSON string inside a JSON string
    return SimpleNamespace(data=json.dumps(json.dumps(data, default=str)))


@pytest.mark.unit
def test_session_keeps_responsibilities():
    session = _session(
        {"scouts_groups": [{"number": "X1201G", "name": "Testgroep", "type": "Groep", "responsibilities": ["leiding"]}]}
    )

    group = ScoutsUserSessionSerializer.to_scouts_user(session)["scouts_groups"][0]

    assert group.number == "X1201G"
    assert group.responsibilities == ["leiding"]


@pytest.mark.unit
def test_old_session_without_responsibilities_is_discarded():
    session = _session(
        {
            "scouts_groups": [{"number": "X1201G", "name": "Testgroep", "_child_group_names": "", "type": "Groep"}],
            "scouts_functions": [],
        }
    )

    assert ScoutsUserSessionSerializer.to_scouts_user(session) == {}
