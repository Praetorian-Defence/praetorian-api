from django.utils.decorators import method_decorator
from django.views import View

from apps.api.auth.decorators import superuser_required
from apps.api.filters.log_entry import LogEntryFilter
from apps.api.response import PaginationResponse
from apps.core.models import LogEntry
from apps.core.serializers.log_entry import LogEntrySerializer


class LogEntryManagement(View):
    @method_decorator(superuser_required)
    def get(self, request):
        log_entries = LogEntryFilter(request.GET, queryset=LogEntry.objects.all(), request=request).qs

        return PaginationResponse(request, log_entries, serializer=LogEntrySerializer.Base)
