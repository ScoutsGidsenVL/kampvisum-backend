"""apps.visums.filters.visum_filter."""
import logging

from django.db.models import Q
from django_filters import rest_framework as filters
from scouts_auth.inuits.logging import InuitsLogger

from apps.camps.services import CampYearService
from apps.visums.models import CampVisum

logger: InuitsLogger = logging.getLogger(__name__)


class CampVisumFilter(filters.FilterSet):
    class Meta:
        model = CampVisum
        fields = []

    @property
    def qs(self):
        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)
        if not year or year == "undefined":
            year = CampYearService().get_or_create_current_camp_year()
            year = year.year

        return CampVisum.objects.get_all_for_group_and_year(group_admin_id=group_admin_id, year=year)
