import django_filters

from apps.core.models import AuditLog


class AuditLogFilter(django_filters.FilterSet):
    user_id = django_filters.CharFilter(method='filter_user')
    device_id = django_filters.CharFilter(method='filter_device')
    remote_id = django_filters.CharFilter(method='filter_remote')
    query = django_filters.CharFilter(method='filter_query')

    class Meta:
        model = AuditLog
        fields = []
