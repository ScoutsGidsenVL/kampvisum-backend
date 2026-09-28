from django.contrib import admin

from apps.camps.services import CampYearService

from scouts_auth.scouts.services import ScoutsPermissionService


class ContentAdminSite(admin.AdminSite):
    """
    Django admin site for managing camp visum content (categories, sub-categories,
    checks, deadlines, ...) and organisational reference data.

    Access is restricted to users in the role_content_admin Django group, which is
    assigned at login to the same groupadmin groups as role_administrator (see
    KNOWN_ADMIN_GROUPS, ScoutsUser.has_role_administrator() and
    ScoutsPermissionService.update_user_authorizations()). It carries its own set of
    change permissions in roles.yaml, which is why it is a distinct Django group from
    role_administrator. is_staff is deliberately not used here, since it is set to True
    for every OIDC user.
    """

    site_header = "Kampvisum beheer"
    site_title = "Kampvisum beheer"
    index_title = "Inhoud beheren"
    login_template = "content_admin/login.html"

    def has_permission(self, request) -> bool:
        user = request.user
        return bool(
            user
            and user.is_active
            and user.groups.filter(name=ScoutsPermissionService.CONTENT_ADMIN).exists()
        )


content_admin_site = ContentAdminSite(name="content_admin")


class DefaultFalseBooleanFilter(admin.SimpleListFilter):
    """
    A boolean field filter that, when unselected, filters to False rather than
    showing everything, with the default choice honestly labelled instead of
    Django's generic "All" ("Alles" is still offered as an explicit choice).

    Subclass and set title, parameter_name (must match the model field name),
    default_label (shown for the unselected/False state) and true_label (shown for
    the True state).
    """

    default_label = "Nee"
    true_label = "Ja"

    def lookups(self, request, model_admin):
        return (
            ("true", self.true_label),
            ("all", "Alles"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "all":
            return queryset
        if value == "true":
            return queryset.filter(**{self.parameter_name: True})
        return queryset.filter(**{self.parameter_name: False})

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string(remove=[self.parameter_name]),
            "display": self.default_label,
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string({self.parameter_name: lookup}),
                "display": title,
            }


class CurrentCampYearFilter(admin.RelatedFieldListFilter):
    """
    Behaves exactly like Django's own RelatedFieldListFilter for a camp-year FK (or
    FK-chain, via CampYearScopedAdminMixin.camp_year_lookup), except the default,
    unselected choice is labelled with the actual current camp year instead of
    Django's generic "All". The unselected state does not show every year, only the
    current one (see CampYearScopedAdminMixin.get_queryset), so calling it "All"
    would be misleading.
    """

    def choices(self, changelist):
        current_year = CampYearService().get_current_camp_year()
        label = f"Huidig ({current_year.year})" if current_year else "Huidig"

        yield {
            "selected": self.lookup_val is None and not self.lookup_val_isnull,
            "query_string": changelist.get_query_string(remove=[self.lookup_kwarg, self.lookup_kwarg_isnull]),
            "display": label,
        }
        for pk_val, val in self.lookup_choices:
            yield {
                "selected": self.lookup_val == str(pk_val),
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg: pk_val}, [self.lookup_kwarg_isnull]
                ),
                "display": val,
            }
        if self.include_empty_choice:
            yield {
                "selected": bool(self.lookup_val_isnull),
                "query_string": changelist.get_query_string(
                    {self.lookup_kwarg_isnull: "True"}, [self.lookup_kwarg]
                ),
                "display": self.empty_value_display,
            }


class CampYearScopedAdminMixin:
    """
    Defaults a changelist to the current camp year, so a content admin does not have
    to scroll through every historical year. Also injects CurrentCampYearFilter for
    camp_year_lookup (a plain field name or FK-chain, e.g. "category__camp_year"), so
    an older year can still be picked explicitly, with the default choice honestly
    labelled instead of "All".
    """

    camp_year_lookup = "camp_year"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        filter_param = f"{self.camp_year_lookup}__id__exact"
        if filter_param in request.GET:
            return queryset

        current_year = CampYearService().get_current_camp_year()
        if current_year is None:
            return queryset

        return queryset.filter(**{self.camp_year_lookup: current_year})

    def get_list_filter(self, request):
        return [(self.camp_year_lookup, CurrentCampYearFilter), *super().get_list_filter(request)]
