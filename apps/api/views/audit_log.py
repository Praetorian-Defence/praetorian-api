from http import HTTPStatus

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException
from apps.api.filters.audit_log import AuditLogFilter
from apps.api.forms.log import LogForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import AuditLog
from apps.core.serializers.audit_log import AuditLogSerializer
from apps.core.services.audit_log import AuditLogService


class AuditLogManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    def post(self, request):
        form = LogForms.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        audit_log = AuditLog()
        form.populate(audit_log)
        audit_log.base_log = {"log": form.cleaned_data['base_log']}
        audit_log.device = request.logged_device
        audit_log.user = request.user

        clean_log_service = AuditLogService.create_from_request(audit_log=audit_log)
        clean_log_service.clean()

        return SingleResponse(request, audit_log, status=HTTPStatus.CREATED, serializer=AuditLogSerializer.Base)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_log'))
    def get(self, request):
        logs = AuditLogFilter(request.GET, queryset=AuditLog.objects.all(), request=request).qs

        return PaginationResponse(request, logs, serializer=AuditLogSerializer.Base)
