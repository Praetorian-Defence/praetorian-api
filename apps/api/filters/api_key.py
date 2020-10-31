import django_filters
from django.db.models import Q

from apps.core.models import ApiKey


class ApiKeyFilter(django_filters.FilterSet):
    platform = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    key = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    secret = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    is_active = django_filters.BooleanFilter()
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = ApiKey
        fields = []

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(platform__unaccent__icontains=value) |
            Q(key__unaccent__icontains=value) |
            Q(secret__unaccent__icontains=value)
        ).distinct()
