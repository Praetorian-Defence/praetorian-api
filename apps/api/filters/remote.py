import django_filters
from django.db.models import Q

from apps.core.models import Remote


class RemoteFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    project_id = django_filters.CharFilter(method='filter_project')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = Remote
        fields = []

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(name__unaccent__icontains=value)
        ).distinct()

    @staticmethod
    def filter_project(qs, name, value):
        return qs.filter(projects=value)
