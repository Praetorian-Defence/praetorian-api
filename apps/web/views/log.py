import logging
from http import HTTPStatus

from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.api.errors import ApiException
from apps.core.models import Log


class LogView(View):
    def get(self, request):
        logs = Log.objects.all().order_by('-created_at')

        data = {
            'logs': logs,
            'log': logs.first()
        }

        if not logs:
            logging.getLogger('logger').info('No log data')
        else:
            logging.getLogger('logger').info('There is data')

        return render(request, 'web/log_list.html', data)


class LogDetail(View):
    def get(self, request, log_id):
        try:
            log = Log.objects.get(pk=log_id)
        except Log.DoesNotExist:
            raise ApiException(request, _('Log does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        data = {'log': log}

        return render(request, 'web/partial_log.html', data)


__all__ = [
    'LogView',
    'LogDetail'
]
