from django_filters import rest_framework as filters
from django.db.models import Q

from apps.camps.models import Camp


# LOGGING
import logging
from scouts_auth.inuits.logging import InuitsLogger

logger: InuitsLogger = logging.getLogger(__name__)


class CampFilter(filters.FilterSet):
    class Meta:
        model = Camp
        fields = []

    @property
    def qs(self):
        parent = super().qs
        group_admin_id = self.request.query_params.get("group", None)
        year = self.request.query_params.get("year", None)

        if year and group_admin_id:
            # logger.debug(
            #     "Filtering Camp instances with group %s and year %s",
            #     group_admin_id,
            #     year,
            # )
            return parent.filter(
                Q(start_date__year=year),
                Q(visum__group__group_admin_id=group_admin_id),
            ).distinct()

        if year:
            # logger.debug("Filtering Camp instances with year %s", year)
            return parent.filter(start_date__year=year)

        if group_admin_id:
            # logger.debug("Filtering Camp instances with group %s", group_admin_id)
            return parent.filter(visum__group__group_admin_id=group_admin_id).distinct()

        # logger.debug("Filters for Camp not set, returning all instances")
        return parent.all()
