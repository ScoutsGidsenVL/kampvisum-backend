from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.core.exceptions import ValidationError

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


class SingleLineTextFieldsMixin:
    """
    Renders the named TextField-backed fields as a single-line text input instead of
    Django's default multi-line textarea. The fields stay TextField at the model and
    database level (no migration, no length limit added), only the admin widget
    changes.
    """

    single_line_fields = ()

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in self.single_line_fields:
            kwargs["widget"] = AdminTextInputWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


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
    labelled instead of "All". A subclass adds its own filters via
    extra_list_filter, not list_filter (see the list_filter property below).
    """

    camp_year_lookup = "camp_year"
    extra_list_filter = ()

    @property
    def list_filter(self):
        # A property, not a plain attribute: ModelAdmin.lookup_allowed() (the check
        # that guards against arbitrary querystring lookups) reads self.list_filter
        # directly, not the overridable get_list_filter(request). Injecting the camp
        # year filter only through get_list_filter() left it "not allowed", causing a
        # 400 on every camp-year filter click for SubCategory and Check (their
        # camp_year_lookup is a multi-level FK chain, so the mismatch showed up
        # there; Category's single-level chain happened not to have been tried yet).
        return [(self.camp_year_lookup, CurrentCampYearFilter), *self.extra_list_filter]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        filter_param = f"{self.camp_year_lookup}__id__exact"
        if filter_param in request.GET:
            return queryset

        current_year = CampYearService().get_current_camp_year()
        if current_year is None:
            return queryset

        return queryset.filter(**{self.camp_year_lookup: current_year})

    def get_object(self, request, object_id, from_field=None):
        # The current-year default in get_queryset() must only narrow the
        # changelist, not object lookups: a direct link to a specific object (an
        # older year reached via the sidebar filter, or simply any object while the
        # current year has nothing yet) must still resolve. Bypasses this mixin's
        # get_queryset() by going through ModelAdmin's own directly.
        queryset = admin.ModelAdmin.get_queryset(self, request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: object_id})
        except (model.DoesNotExist, ValidationError, ValueError):
            return None
