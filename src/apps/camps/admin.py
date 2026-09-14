from django.contrib import admin, messages

from apps.camps.models import CampYear
from apps.camps.services import CampYearCloneService

from scouts_kampvisum_api.admin import content_admin_site


@admin.register(CampYear, site=content_admin_site)
class CampYearAdmin(admin.ModelAdmin):
    list_display = ("year", "start_date", "end_date")
    ordering = ("-year",)
    readonly_fields = ("year", "start_date", "end_date")
    actions = ["clone_to_next_year"]

    def has_add_permission(self, request) -> bool:
        # CampYear rows are created automatically (CampYearService.get_or_create_
        # current_camp_year / setupcampyears), never by hand.
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.action(description="Kloon naar volgend jaar")
    def clone_to_next_year(self, request, queryset):
        # Deliberately ignores the selected rows: the target and source year are
        # always computed the same way, see CampYearCloneService.
        message, cloned = CampYearCloneService().clone_to_current_year()
        self.message_user(request, message, level=messages.SUCCESS if cloned else messages.WARNING)
