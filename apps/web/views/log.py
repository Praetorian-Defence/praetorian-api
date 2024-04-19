import base64
import json
import logging
from http import HTTPStatus

from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.api.errors import ApiException
from apps.core.models import AuditLog


class LogView(View):
    def get(self, request):
        logs = AuditLog.objects.all().order_by('-created_at')

        first_log = decode_data(logs.first())

        data = {
            'logs': logs,
            'log': first_log
        }

        if not logs:
            logging.getLogger('logger').info('No log data')
        else:
            logging.getLogger('logger').info('There is data')

        return render(request, 'web/log_list.html', data)


class LogDetail(View):
    def get(self, request, log_id):
        try:
            log = AuditLog.objects.get(pk=log_id)
        except AuditLog.DoesNotExist:
            raise ApiException(request, _('Log does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        data = {'log': decode_data(log)}

        return render(request, 'web/partial_log.html', data)


def decode_data(log: AuditLog) -> AuditLog:
    decoded_data = base64.b64decode(log.cleaned_log['log']).decode('utf-8')
    log.cleaned_log['log'] = json.loads(decoded_data)

    return log


__all__ = [
    'LogView',
    'LogDetail'
]
