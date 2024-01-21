import django_filters
from django.db.models import Q
from django_enum_choices.filters import EnumChoiceFilter

from apps.core.models import ApiKey


class ApiKeyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    type = EnumChoiceFilter(ApiKey.ApiKeyType)
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
            Q(name__icontains=value)
            | Q(type__icontains=value)
            | Q(key__icontains=value)
            | Q(secret__icontains=value)
        ).distinct()
