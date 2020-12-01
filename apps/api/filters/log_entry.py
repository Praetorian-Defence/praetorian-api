import django_filters
from django.db.models import Q

from apps.core.models import LogEntry


class LogEntryFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.CharFilter(lookup_expr='icontains')
    message = django_filters.CharFilter(lookup_expr='icontains')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = LogEntry
        fields = []

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(username__icontains=value) |
            Q(level__icontains=value) |
            Q(message__icontains=value)
        ).distinct()
