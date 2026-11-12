from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from apps.visums.models import Category, SubCategory, Check
from apps.visums.services import TemplateArchiveService

from scouts_kampvisum_api.admin import (
    content_admin_site,
    CampYearLockMixin,
    CampYearScopedAdminMixin,
    DefaultFalseBooleanFilter,
    SingleLineTextFieldsMixin,
)

LOCKED_YEAR_MESSAGE = "Niets gewijzigd: een geselecteerd item hoort bij een afgesloten kampjaar."


class ArchivedFilter(DefaultFalseBooleanFilter):
    title = "archief"
    parameter_name = "is_archived"
    default_label = "Niet gearchiveerd"
    true_label = "Enkel gearchiveerd"


class ArchiveActionsMixin:
    actions = ["archive_selected", "restore_selected"]

    @admin.action(description="Archiveer")
    def archive_selected(self, request, queryset):
        if self.includes_locked_year(request, queryset):
            self.message_user(request, LOCKED_YEAR_MESSAGE, level=messages.ERROR)
            return
        try:
            TemplateArchiveService().archive(queryset, request.user)
        except ValidationError as error:
            self.message_user(request, " ".join(error.messages), level=messages.ERROR)

    @admin.action(description="Herstel")
    def restore_selected(self, request, queryset):
        if self.includes_locked_year(request, queryset):
            self.message_user(request, LOCKED_YEAR_MESSAGE, level=messages.ERROR)
            return
        TemplateArchiveService().restore(queryset)


@admin.register(Category, site=content_admin_site)
class CategoryAdmin(
    SingleLineTextFieldsMixin, CampYearScopedAdminMixin, CampYearLockMixin, ArchiveActionsMixin, admin.ModelAdmin
):
    camp_year_lookup = "camp_year"
    single_line_fields = ("label", "description")

    list_display = ("name", "camp_year", "label", "is_archived")
    extra_list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "camp_year", "label", "description", "explanation")
    readonly_fields = ("name", "camp_year")

    def has_add_permission(self, request) -> bool:
        # Categories are created by cloning a camp year (CampYearCloneService), not by
        # hand.
        return False


@admin.register(SubCategory, site=content_admin_site)
class SubCategoryAdmin(
    SingleLineTextFieldsMixin, CampYearScopedAdminMixin, CampYearLockMixin, ArchiveActionsMixin, admin.ModelAdmin
):
    camp_year_lookup = "category__camp_year"
    single_line_fields = ("label", "description")

    list_display = ("name", "category", "label", "is_archived")
    extra_list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "category", "label", "description", "explanation", "link")
    readonly_fields = ("name", "category")

    def has_add_permission(self, request) -> bool:
        return False


@admin.register(Check, site=content_admin_site)
class CheckAdmin(
    SingleLineTextFieldsMixin, CampYearScopedAdminMixin, CampYearLockMixin, ArchiveActionsMixin, admin.ModelAdmin
):
    camp_year_lookup = "sub_category__category__camp_year"
    single_line_fields = ("label",)

    list_display = ("name", "sub_category", "check_type", "label", "is_archived")
    extra_list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "sub_category", "check_type", "label", "explanation", "link")
    readonly_fields = ("name", "sub_category", "check_type")

    def has_add_permission(self, request) -> bool:
        return False
