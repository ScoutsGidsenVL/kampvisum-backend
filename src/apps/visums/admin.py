from django.contrib import admin
from django.utils import timezone

from apps.visums.models import Category, SubCategory, Check

from scouts_kampvisum_api.admin import (
    content_admin_site,
    CampYearScopedAdminMixin,
    DefaultFalseBooleanFilter,
)


class ArchivedFilter(DefaultFalseBooleanFilter):
    title = "archief"
    parameter_name = "is_archived"
    default_label = "Niet gearchiveerd"
    true_label = "Enkel gearchiveerd"


class ArchiveActionsMixin:
    actions = ["archive_selected", "restore_selected"]

    @admin.action(description="Archiveer")
    def archive_selected(self, request, queryset):
        queryset.update(is_archived=True, archived_by=request.user, archived_on=timezone.now())

    @admin.action(description="Herstel")
    def restore_selected(self, request, queryset):
        queryset.update(is_archived=False, archived_by=None, archived_on=None)


@admin.register(Category, site=content_admin_site)
class CategoryAdmin(CampYearScopedAdminMixin, ArchiveActionsMixin, admin.ModelAdmin):
    camp_year_lookup = "camp_year"

    list_display = ("name", "camp_year", "label", "is_archived")
    list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "camp_year", "label", "description", "explanation")
    readonly_fields = ("name", "camp_year")

    def has_add_permission(self, request) -> bool:
        # Categories are created by cloning a camp year (CampYearCloneService), not by
        # hand.
        return False


@admin.register(SubCategory, site=content_admin_site)
class SubCategoryAdmin(CampYearScopedAdminMixin, ArchiveActionsMixin, admin.ModelAdmin):
    camp_year_lookup = "category__camp_year"

    list_display = ("name", "category", "label", "is_archived")
    list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "category", "label", "description", "explanation", "link")
    readonly_fields = ("name", "category")

    def has_add_permission(self, request) -> bool:
        return False


@admin.register(Check, site=content_admin_site)
class CheckAdmin(CampYearScopedAdminMixin, ArchiveActionsMixin, admin.ModelAdmin):
    camp_year_lookup = "sub_category__category__camp_year"

    list_display = ("name", "sub_category", "check_type", "label", "is_archived")
    list_filter = (ArchivedFilter,)
    search_fields = ("name",)
    fields = ("name", "sub_category", "check_type", "label", "explanation", "link")
    readonly_fields = ("name", "sub_category", "check_type")

    def has_add_permission(self, request) -> bool:
        return False
