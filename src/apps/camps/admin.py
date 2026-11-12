import datetime

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse
from django.utils.functional import lazy

from apps.camps.models import CampYear
from apps.camps.services import CampYearCloneService
from apps.visums.models import Category

from scouts_auth.scouts.util import ScoutsTemporalDetails

from scouts_kampvisum_api.admin import content_admin_site


def clone_label() -> str:
    # Names the years: the camp year spans two calendar years, so "previous" or "next" is ambiguous.
    target_year = ScoutsTemporalDetails.get_end_of_camp_year(datetime.date.today()).year
    return f"Kloon kampjaar {target_year - 1} naar kampjaar {target_year}"


@admin.register(CampYear, site=content_admin_site)
class CampYearAdmin(admin.ModelAdmin):
    list_display = ("year", "start_date", "end_date")
    ordering = ("-year",)
    # The audit fields are left out: CampYear rows are created by the system without a
    # request, so created_by/updated_by are always empty.
    fields = ("year", "start_date", "end_date")
    actions = ["clone_previous_year"]

    def has_add_permission(self, request) -> bool:
        # CampYear rows are created automatically (CampYearService.get_or_create_
        # current_camp_year / setupcampyears), never by hand.
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        # A camp year is fully computed, so there is nothing to edit. The detail page
        # is shown read-only; the clone action on the changelist keeps working.
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    @admin.action(description=lazy(clone_label, str)())
    def clone_previous_year(self, request, queryset):
        # Deliberately ignores the selected rows: the target and source year are
        # always computed the same way, see CampYearCloneService.
        if request.POST.get("post"):
            try:
                message, cloned = CampYearCloneService().clone_to_current_year(user=request.user)
                level = messages.SUCCESS if cloned else messages.WARNING
            except ValidationError as error:
                message, level = " ".join(error.messages), messages.ERROR
            self.message_user(request, message, level=level)
            return None

        start_date, end_date = ScoutsTemporalDetails.get_start_and_end_date_of_camp_year(datetime.date.today())
        return TemplateResponse(
            request,
            "admin/camps/campyear/clone_confirmation.html",
            {
                **self.admin_site.each_context(request),
                "title": "Kampjaar klonen",
                "opts": self.model._meta,
                "queryset": queryset,
                "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
                "source_year": end_date.year - 1,
                "target_year": end_date.year,
                "start_date": start_date,
                "end_date": end_date,
                "next_start_date": end_date + datetime.timedelta(days=1),
                "has_content": Category.objects.filter(camp_year__year=end_date.year).exists(),
            },
        )
