import django_filters
from django.db.models import Q

from apps.core.models import ApiKey


class ApiKeyFilter(django_filters.FilterSet):
    platform = django_filters.CharFilter(lookup_expr='icontains')
    key = django_filters.CharFilter(lookup_expr='icontains')
    secret = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = ApiKey
        fields = []

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(platform__icontains=value) |
            Q(key__icontains=value) |
            Q(secret__icontains=value)
        ).distinct()
