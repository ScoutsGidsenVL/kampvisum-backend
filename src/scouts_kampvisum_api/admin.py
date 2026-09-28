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


class CampYearScopedAdminMixin:
    """
    Defaults a changelist to the current camp year, so a content admin does not have
    to scroll through every historical year. The list_filter entry for
    camp_year_lookup (a plain field name or FK-chain, e.g. "category__camp_year") lets
    an older year still be picked explicitly.
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
