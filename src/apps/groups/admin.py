from django.contrib import admin

from apps.groups.models import DefaultScoutsSectionName

from scouts_kampvisum_api.admin import content_admin_site, DefaultFalseBooleanFilter


# ScoutsGroupType is not registered here: it is sourced from the groupadmin, not
# managed in this admin.


class HiddenFilter(DefaultFalseBooleanFilter):
    title = "zichtbaarheid"
    parameter_name = "hidden"
    default_label = "Niet verborgen"
    true_label = "Enkel verborgen"


@admin.register(DefaultScoutsSectionName, site=content_admin_site)
class DefaultScoutsSectionNameAdmin(admin.ModelAdmin):
    list_display = ("name", "group_type", "gender", "age_group", "hidden")
    list_filter = ("group_type", "gender", "age_group", HiddenFilter)
    search_fields = ("name",)
