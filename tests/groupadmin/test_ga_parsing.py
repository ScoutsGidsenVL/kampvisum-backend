"""
Unit tests for GA API response parsing.

Each test provides a minimal GA JSON fixture (using Dutch field names as returned
by the GA API) and asserts the parsed Python object has the expected field values.
These tests lock in current serializer behaviour before the Pydantic migration.
"""
import pytest

from scouts_auth.groupadmin.serializers.value_objects import (
    GaLinkSerializer,
    GaGroupSerializer,
    GaMemberFunctionSerializer,
    GaFunctionDescriptionSerializer,
    GaListMemberSerializer,
    GaListMemberPageSerializer,
    GaSearchMemberSerializer,
    GaSearchMemberPageSerializer,
)
from scouts_auth.groupadmin.serializers.value_objects.ga_profile_member_serializer import (
    GaMemberPersonalDataSerializer,
    GaMemberGroupAdminDataSerializer,
    GaMemberScoutsDataSerializer,
    GaMemberSerializer,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse(serializer_class, data: dict, many: bool = False):
    """Call to_internal_value + create on a copy of data (serializers pop from the dict)."""
    s = serializer_class(many=many)
    validated = s.to_internal_value(data.copy() if not many else data)
    return s.create(validated)


# ---------------------------------------------------------------------------
# GaLink
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_link_parsing():
    data = {"rel": "self", "href": "https://ga.example.com/lid/1", "method": "GET", "secties": []}
    link = _parse(GaLinkSerializer, data)
    assert link.rel == "self"
    assert link.href == "https://ga.example.com/lid/1"
    assert link.method == "GET"


# ---------------------------------------------------------------------------
# GaGroup
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_group_parsing_minimal():
    data = {"id": "A1234B", "naam": "Test Scouts", "soort": "groep", "links": []}
    group = _parse(GaGroupSerializer, data)
    assert group.group_admin_id == "A1234B"
    assert group.name == "Test Scouts"
    assert group.type == "groep"


@pytest.mark.unit
def test_ga_group_parsing_with_parent():
    data = {
        "id": "A1234B",
        "naam": "Test Scouts",
        "soort": "groep",
        "bovenliggendeGroep": "A1234",
        "onderliggendeGroepen": ["A1234G", "A1234M"],
        "links": [],
    }
    group = _parse(GaGroupSerializer, data)
    assert group.parent_group == "A1234"
    assert group.child_groups == ["A1234G", "A1234M"]


# ---------------------------------------------------------------------------
# GaMemberFunction
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_member_function_parsing():
    data = {
        "groep": "A1234B",
        "functie": "abc-123",
        "begin": "2023-09-01T00:00:00",
        "code": "GVL",
        "omschrijving": "Gidsen-verkennerleiding",
        "links": [],
    }
    fn = _parse(GaMemberFunctionSerializer, data)
    assert fn.function == "abc-123"
    assert fn.scouts_group.group_admin_id == "A1234B"
    assert fn.code == "GVL"
    assert fn.description == "Gidsen-verkennerleiding"
    assert fn.end is None


@pytest.mark.unit
def test_ga_member_function_parsing_with_end_date():
    data = {
        "groep": "A1234B",
        "functie": "abc-123",
        "begin": "2020-09-01T00:00:00",
        "einde": "2021-06-30T00:00:00",
        "code": "GVL",
        "omschrijving": "Gidsen-verkennerleiding",
        "links": [],
    }
    fn = _parse(GaMemberFunctionSerializer, data)
    assert fn.end is not None


# ---------------------------------------------------------------------------
# GaFunctionDescription
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_function_description_parsing():
    data = {
        "id": "abc-123",
        "type": "sectie",
        "code": "GVL",
        "omschrijving": "Gidsen-verkennerleiding",
        "groeperingen": [{"naam": "Leiding", "volgorde": 1}],
        "groepen": [],
        "links": [],
    }
    desc = _parse(GaFunctionDescriptionSerializer, data)
    assert desc.group_admin_id == "abc-123"
    assert desc.code == "GVL"
    assert desc.description == "Gidsen-verkennerleiding"
    assert len(desc.groupings) == 1
    assert desc.groupings[0].name == "Leiding"


@pytest.mark.unit
def test_ga_function_description_non_leader():
    data = {
        "id": "def-456",
        "type": "nationaal",
        "code": "LID",
        "omschrijving": "Lid",
        "groeperingen": [{"naam": "Leden", "volgorde": 1}],
        "groepen": [],
        "links": [],
    }
    desc = _parse(GaFunctionDescriptionSerializer, data)
    assert desc.groupings[0].name == "Leden"


# ---------------------------------------------------------------------------
# GaListMember
# ---------------------------------------------------------------------------

GA_COL_FIRST_NAME = "be.vvksm.groepsadmin.model.column.VoornaamColumn"
GA_COL_LAST_NAME = "be.vvksm.groepsadmin.model.column.AchternaamColumn"


@pytest.mark.unit
def test_ga_list_member_parsing():
    data = {
        "id": "12345",
        "positie": 0,
        "waarden": {
            GA_COL_FIRST_NAME: "Jan",
            GA_COL_LAST_NAME: "Janssen",
        },
        "links": [],
    }
    member = _parse(GaListMemberSerializer, data)
    assert member.group_admin_id == "12345"
    assert member.index == 0
    values_by_key = {v.key: v.value for v in member.values}
    assert values_by_key[GA_COL_FIRST_NAME] == "Jan"
    assert values_by_key[GA_COL_LAST_NAME] == "Janssen"


# ---------------------------------------------------------------------------
# GaListMemberPage
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_list_member_page_parsing():
    data = {
        "aantal": 1,
        "totaal": 1,
        "offset": 0,
        "leden": [
            {
                "id": "12345",
                "positie": 0,
                "waarden": {GA_COL_FIRST_NAME: "Jan"},
                "links": [],
            }
        ],
        "links": [],
    }
    s = GaListMemberPageSerializer(data=data.copy())
    page = s.save()
    assert page.count == 1
    assert page.total == 1
    assert len(page.members) == 1
    assert page.members[0].group_admin_id == "12345"


# ---------------------------------------------------------------------------
# GaSearchMember
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_search_member_parsing():
    data = {
        "id": "12345",
        "voornaam": "Jan",
        "achternaam": "Janssen",
        "geboortedatum": "1995-03-15",
        "email": "jan@example.com",
        "gsm": "+32477000000",
        "links": [],
    }
    member = _parse(GaSearchMemberSerializer, data)
    assert member.group_admin_id == "12345"
    assert member.first_name == "Jan"
    assert member.last_name == "Janssen"
    assert member.email == "jan@example.com"
    assert member.phone_number == "+32477000000"


# ---------------------------------------------------------------------------
# GaSearchMemberPage
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_search_member_page_parsing():
    data = {
        "aantal": 1,
        "totaal": 5,
        "offset": 0,
        "leden": [
            {
                "id": "12345",
                "voornaam": "Jan",
                "achternaam": "Janssen",
                "geboortedatum": "1995-03-15",
                "email": "jan@example.com",
                "links": [],
            }
        ],
        "links": [],
    }
    s = GaSearchMemberPageSerializer(data=data.copy())
    page = s.save()
    assert page.count == 1
    assert page.total == 5
    assert len(page.members) == 1
    assert page.members[0].first_name == "Jan"


# ---------------------------------------------------------------------------
# GaProfileMember (full profile)
# ---------------------------------------------------------------------------

@pytest.mark.unit
def test_ga_profile_member_parsing():
    data = {
        "id": "12345",
        "gebruikersnaam": "jan.janssen",
        "email": "jan@example.com",
        "persoonsgegevens": {"geslacht": "M", "gsm": "+32477000000"},
        "vgagegevens": {
            "voornaam": "Jan",
            "achternaam": "Janssen",
            "geboortedatum": "1995-03-15",
        },
        "verbondsgegevens": {"lidnummer": "LID123", "klantnummer": "KLANT456"},
        "functies": [],
        "groepen": [],
        "adressen": [],
        "contacten": [],
        "groepseigenVelden": {},
        "links": [],
    }
    s = GaMemberSerializer(data=data.copy())
    s.is_valid(raise_exception=True)
    member = s.save()

    assert member.group_admin_id == "12345"
    assert member.username == "jan.janssen"
    assert member.email == "jan@example.com"
    assert member.first_name == "Jan"
    assert member.last_name == "Janssen"
    assert member.phone_number == "+32477000000"
    assert member.membership_number == "LID123"
    assert member.customer_number == "KLANT456"


@pytest.mark.unit
def test_ga_profile_member_with_function():
    data = {
        "id": "12345",
        "gebruikersnaam": "jan.janssen",
        "email": "jan@example.com",
        "persoonsgegevens": {"geslacht": "M", "gsm": ""},
        "vgagegevens": {"voornaam": "Jan", "achternaam": "Janssen", "geboortedatum": "1995-03-15"},
        "verbondsgegevens": {"lidnummer": "", "klantnummer": ""},
        "functies": [
            {
                "groep": "A1234B",
                "functie": "abc-123",
                "begin": "2023-09-01T00:00:00",
                "code": "GVL",
                "omschrijving": "Gidsen-verkennerleiding",
                "links": [],
            }
        ],
        "groepen": [],
        "adressen": [],
        "contacten": [],
        "groepseigenVelden": {},
        "links": [],
    }
    s = GaMemberSerializer(data=data.copy())
    s.is_valid(raise_exception=True)
    member = s.save()

    assert len(member.functions) == 1
    assert member.functions[0].code == "GVL"
    assert member.functions[0].scouts_group.group_admin_id == "A1234B"
