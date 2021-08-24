import requests, logging
from django.db import models
from django.conf import settings

logger = logging.getLogger(__name__)
base_endpoint = settings.GROUP_ADMIN_BASE_ENDPOINT


class GroupAdminApi:
    """
    Constructs endpoints for various GroupAdmin API calls.
    """
    
    default_scouts_group_type = 'Groep'
    
    @staticmethod
    def get_request(endpoint: str, active_user):
        #return requests.get("{0}".format(endpoint),
        #    headers={"Authorization": "Bearer {0}".format(
        #        active_user.access_token)},
        #)
        return requests.get(endpoint)
    
    @staticmethod
    def get_groups_endpoint():
        """
        Return all groups for which the user has rights.
        
        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        
        return base_endpoint + '/groep'


class MemberGender(models.TextChoices):
    # For people
    OTHER = 'X', 'Other'
    FEMALE = 'F', 'Female'
    MALE = 'M', 'Male'
    # To specify a scouts group that is gender-mixed
    MIXED = 'H', 'Mixed'

class AgeGroup(models.TextChoices):
    # Kapoenen, zeehondjes
    AGE_GROUP_1 = (
        '10', 'Leeftijdsgroep 6-9: kapoenen en zeehondjes'
    )
    AGE_GROUP_1_07 = (
        '15', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 7 jaar'
    )
    AGE_GROUP_1_08 = (
        '16', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 8 jaar'
    )
    AGE_GROUP_1_09 = (
        '17', 'Tussentak, leeftijdsgroep 6-9: startleeftijd 9 jaar'
    )
    AGE_GROUP_2 = (
        '20', 'Leeftijdsgroep 8-11: kabouter en (zee)welp'
    )
    AGE_GROUP_2_09 = (
        '25', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 9 jaar'
    )
    AGE_GROUP_2_10 = (
        '26', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 10 jaar'
    )
    AGE_GROUP_2_11 = (
        '27', 'Tussentak, leeftijdsgroep 8-11: startleeftijd 11 jaar'
    )
    AGE_GROUP_3 = (
        '30', 'Leeftijdsgroep 11-14: jonggivers en scheepsmakkers'
    )
    AGE_GROUP_3_12 = (
        '35', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 12 jaar'
    )
    AGE_GROUP_3_13 = (
        '36', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 13 jaar'
    )
    AGE_GROUP_3_14 = (
        '37', 'Tussentak, leeftijdsgroep 11-14: startleeftijd 14 jaar'
    )
    AGE_GROUP_4 = (
        '40', 'Leeftijdsgroep 14-17: gidsen en (zee)verkenners'
    )
    AGE_GROUP_4_15 = (
        '45', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 15 jaar'
    )
    AGE_GROUP_4_16 = (
        '46', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 16 jaar'
    )
    AGE_GROUP_4_17 = (
        '47', 'Tussentak, leeftijdsgroep 14-17: startleeftijd 17 jaar'
    )
    AGE_GROUP_5 = (
        '50', 'Leeftijdsgroep 17-18: jins en loodsen'
    )
    AGE_GROUP_5_18 = (
        '55', 'Tussentak, leeftijdsgroep 17-18: startleeftijd 18 jaar'
    )
    AGE_GROUP_AFTER_5 = (
        '60', 'Leeftijdsgroep ouder dan 18, bv. VIPS (akabe)'
    )
    AGE_GROUP_6 = (
        '100', 'Leeftijdsgroep voor leiding, district, gouw, verbond'
    )
    AGE_GROUP_UNKNOWN = (
        '999', 'Onbekende leeftijdsgroep'
    )

