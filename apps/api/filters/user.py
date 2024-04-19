import django_filters
from django.db.models import Q

from apps.core.models import User


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = User
        fields = []

    @property
    def qs(self):
        return super().qs

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(name__icontains=value)
            | Q(surname__icontains=value)
        ).distinct()
