from django.contrib import admin

from apps.deadlines.models import Deadline, DeadlineDate

from scouts_kampvisum_api.admin import content_admin_site, CampYearScopedAdminMixin


class DeadlineDateInline(admin.TabularInline):
    # TabularInline rather than StackedInline: a stacked inline shows a
    # "{verbose_name}: {str(instance)}" header per form, and DeadlineDate has no
    # meaningful __str__, giving a raw "DeadlineDate object (<uuid>)" label. A tabular
    # inline has no such header.
    model = DeadlineDate
    can_delete = False
    max_num = 1
    fields = ("date_day", "date_month", "date_year", "calculated_date")
    readonly_fields = ("calculated_date",)


@admin.register(Deadline, site=content_admin_site)
class DeadlineAdmin(CampYearScopedAdminMixin, admin.ModelAdmin):
    list_display = ("name", "camp_year", "label")
    search_fields = ("name",)
    fields = ("name", "camp_year", "label", "description", "explanation")
    readonly_fields = ("name", "camp_year")
    inlines = [DeadlineDateInline]

    def has_add_permission(self, request) -> bool:
        # Deadlines are created by cloning a camp year (CampYearCloneService), not by
        # hand.
        return False

    def save_formset(self, request, form, formset, change):
        # Imported here: a module-level import of apps.deadlines.services creates an
        # import cycle via apps.visums.services back into apps.deadlines.services (see
        # CampYearCloneService._clone for the same fix).
        from apps.deadlines.services import DeadlineService

        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, DeadlineDate):
                instance.calculated_date = DeadlineService().get_calculated_date(
                    day=instance.date_day,
                    month=instance.date_month,
                    year=instance.date_year,
                )
            instance.save()

        formset.save_m2m()
