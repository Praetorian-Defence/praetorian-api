import json
import logging
from http import HTTPStatus

from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException
from apps.api.filters.device import DeviceFilter
from apps.api.forms.device import DeviceForms
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import Device
from apps.core.serializers.device import DeviceSerializer


class DeviceManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_device'))
    def post(self, request):
        form = DeviceForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        device = Device()
        form.fill(device)
        device.save()

        logging.getLogger('logger').info(
            _('Vytvorenie nového zariadenia s názvom {device_name}, používateľom {user_name}.'.format(
                device_name=device.name,
                user_name=request.user.username
            )),
            extra={
                'status_code': HTTPStatus.CREATED,
                'request_body': json.loads(request.body),
                'username': request.user.username
            }
        )

        return SingleResponse(request, device, status=HTTPStatus.CREATED, serializer=DeviceSerializer.Base)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_device'))
    def get(self, request):
        users = DeviceFilter(request.GET, queryset=Device.objects.all(), request=request).qs

        return PaginationResponse(request, users, serializer=DeviceSerializer.Base)
