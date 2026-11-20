"""
Tests for GroupAdmin.get_member_list_filtered().

The GA call itself is mocked: these tests cover what the service adds on top of the parsed response.
"""
import pytest

from scouts_auth.groupadmin.services.group_admin import GroupAdmin


GA_COL_FIRST_NAME = "be.vvksm.groepsadmin.model.column.VoornaamColumn"


@pytest.mark.unit
@pytest.mark.parametrize("oudleden", [False, True])
def test_get_member_list_filtered_sets_active_member(mocker, oudleden):
    json_data = {
        "aantal": 2,
        "totaal": 2,
        "offset": 0,
        "leden": [
            {"id": "12345", "positie": 0, "waarden": {GA_COL_FIRST_NAME: "Jan"}, "links": []},
            {"id": "67890", "positie": 1, "waarden": {GA_COL_FIRST_NAME: "Piet"}, "links": []},
        ],
        "links": [],
    }
    mocker.patch.object(GroupAdmin, "get_member_list_filtered_raw", return_value=json_data)

    page = GroupAdmin().get_member_list_filtered(active_user=mocker.Mock(), oudleden=oudleden)

    assert len(page.members) == 2
    assert all(member.active_member is not oudleden for member in page.members)
