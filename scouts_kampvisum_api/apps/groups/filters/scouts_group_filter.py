"""apps.groups.filters.scouts_group_filter."""

import django_filters
from scouts_auth.groupadmin.models import AbstractScoutsGroup


class ScoutsGroupFilter(django_filters.rest_framework.FilterSet):
    group = django_filters.rest_framework.CharFilter(method="search_group")

    class Meta:
        model = AbstractScoutsGroup
        fields = []

    @property
    def qs(self):
        return super().qs

    def search_group(self, queryset, name, value):
        # return self.qs.all()
        return []
