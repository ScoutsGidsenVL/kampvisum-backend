from django.db import models

from apps.base.models import BaseModel


class ScoutsCampVisumCheck(BaseModel):
    
    name = models.CharField(max_length=64)
    
    def clean(self):
        pass
