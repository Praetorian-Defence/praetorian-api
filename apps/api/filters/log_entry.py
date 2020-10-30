import django_filters
from django.db.models import Q

from apps.core.models import Device


class LogEntryFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    level = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    message = django_filters.CharFilter(lookup_expr='unaccent__icontains')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = Device
        fields = []

    @property
    def qs(self):
        queryset = super().qs
        user = getattr(self.request, 'user', None)

        return queryset

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(username__unaccent__icontains=value) |
            Q(level__unaccent__icontains=value) |
            Q(message__unaccent__icontains=value)
        ).distinct()
