"""apps.groups.filters.scouts_section_filter."""

import django_filters
from apps.groups.models import ScoutsSection


class ScoutsSectionFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = ScoutsSection
        fields = []

    @property
    def qs(self):
        return ScoutsSection.objects.filter(hidden=False)
