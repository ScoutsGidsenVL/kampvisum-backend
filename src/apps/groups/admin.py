from django.contrib import admin

from apps.groups.models import DefaultScoutsSectionName

from scouts_kampvisum_api.admin import content_admin_site


# ScoutsGroupType is not registered here: it is sourced from the groupadmin, not
# managed in this admin.


@admin.register(DefaultScoutsSectionName, site=content_admin_site)
class DefaultScoutsSectionNameAdmin(admin.ModelAdmin):
    list_display = ("name", "group_type", "gender", "age_group", "hidden")
    list_filter = ("group_type", "gender", "hidden")
    search_fields = ("name",)
