from http import HTTPStatus

from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.filters.log import LogFilter
from apps.api.forms.log import LogForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import Log
from apps.core.serializers.log import LogSerializer
from apps.core.services.clean_log import CleanLogService


class LogManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    def post(self, request):
        form = LogForms.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        log = Log()
        form.fill(log)
        log.base_log = {"log": form.cleaned_data['base_log']}
        log.device = request.logged_device
        log.user = request.user

        clean_log_service = CleanLogService.create_from_request(log=log)
        clean_log_service.clean()

        return SingleResponse(request, log, status=HTTPStatus.CREATED, serializer=LogSerializer.Base)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_log'))
    def get(self, request):
        logs = LogFilter(request.GET, queryset=Log.objects.all(), request=request).qs

        return PaginationResponse(request, logs, serializer=LogSerializer.Base)
