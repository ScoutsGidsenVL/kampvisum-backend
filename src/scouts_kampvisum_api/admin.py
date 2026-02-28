from django.contrib import admin

from scouts_auth.groupadmin.models import ScoutsUser
from apps.camps.models import Camp, CampYear
from apps.visums.models import CampVisum


admin.site.register(ScoutsUser)
admin.site.register(Camp)
admin.site.register(CampYear)
admin.site.register(CampVisum)
