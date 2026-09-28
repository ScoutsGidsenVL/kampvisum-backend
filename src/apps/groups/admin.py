from django.contrib import admin

from apps.groups.models import ScoutsGroupType, DefaultScoutsSectionName

from scouts_kampvisum_api.admin import content_admin_site


@admin.register(ScoutsGroupType, site=content_admin_site)
class ScoutsGroupTypeAdmin(admin.ModelAdmin):
    list_display = ("group_type", "parent", "is_default")
    search_fields = ("group_type",)


@admin.register(DefaultScoutsSectionName, site=content_admin_site)
class DefaultScoutsSectionNameAdmin(admin.ModelAdmin):
    list_display = ("name", "group_type", "gender", "age_group", "hidden")
    list_filter = ("group_type", "gender", "hidden")
    search_fields = ("name",)
