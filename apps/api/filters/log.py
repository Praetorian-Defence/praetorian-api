import django_filters

from django.db.models import Q

from apps.core.models import Service


class LogFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(method='filter_user')
    device_id = django_filters.CharFilter(method='filter_device')
    remote_id = django_filters.CharFilter(method='filter_remote')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = Service
        fields = []

    @staticmethod
    def filter_remote(qs, name, value):
        return qs.filter(remote__id=value)

    @staticmethod
    def filter_user(qs, name, value):
        return qs.filter(user__id=value)

    @staticmethod
    def filter_device(qs, name, value):
        return qs.filter(device__id=value)

    @staticmethod
    def filter_query(qs, name, value):
        return qs.filter(
            Q(user__username__icontains=value)
            | Q(user__name__icontains=value)
            | Q(user__surname__icontains=value)
            | Q(user__email__icontains=value)
            | Q(remote__name__icontains=value)
            | Q(device__name__icontains=value)
        ).distinct()
