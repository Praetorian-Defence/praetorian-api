import django_filters

from django_enum_choices.filters import EnumChoiceFilter
from django.db.models import Q

from apps.core.models import Service


class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='exact')
    type = EnumChoiceFilter(Service.ServiceType)
    remote_id = django_filters.CharFilter(method='filter_remote')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = Service
        fields = []

    @staticmethod
    def filter_remote(qs, name, value):
        return qs.filter(remote__id=value)

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(name__icontains=value)
        ).distinct()
