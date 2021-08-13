import requests, logging
from django.conf import settings

from ..scouts_groups.api.groups.models import ScoutsGroup

logger = logging.getLogger(__name__)

class GroupAdminService:
    
    def get_group(
            self, href: str) -> ScoutsGroup:
        response = requests.get(href)
        
        response.raise_for_status()
        json = response.json()
        
        logger.info("GROUP")
        logger.info(json)
        
        addresses = json.get('adressen', [])
        
        return None
    
    def get_groups(self, groups):
        settings
        response = requests.get()
        logger.info('GROUPS: %s', groups)
        
        return None
