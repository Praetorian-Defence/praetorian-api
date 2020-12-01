import django_filters
from django.db.models import Q

from apps.core.models import Project


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    user_id = django_filters.CharFilter(method='filter_user')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = Project
        fields = []

    @staticmethod
    def filter_user(qs, name, value):
        return qs.filter(users_devices__user=value)

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(name__icontains=value)
        ).distinct()
