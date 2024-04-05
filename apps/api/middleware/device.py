from http import HTTPStatus
from typing import Tuple

from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from django.utils.translation import gettext as _

from apps.api.errors import ApiException
from apps.core.models import Device


class DeviceMiddleware(object):
    @staticmethod
    def _get_logged_device(user, request) -> Tuple[Device, str]:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        logged_device = None

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        devices = user.my_devices.all()
        for device in devices:
            if device.ip_address == ip_address:
                logged_device = device

        if not logged_device:
            logged_device, created = Device.objects.get_or_create(user=user, ip_address=ip_address, certificate=ip_address)

        return logged_device, ip_address

    def __init__(self, get_response):
        self.get_response = get_response

    @transaction.atomic
    def __call__(self, request):
        if request.user and not isinstance(request.user, AnonymousUser):
            logged_device, ip_address = self._get_logged_device(request.user, request)

            if logged_device is not None:
                request.logged_device = logged_device
            else:
                raise ApiException(
                    request, _(f'You are trying to connect from a unknown device {ip_address}.'),
                    status_code=HTTPStatus.FORBIDDEN
                )

        return self.get_response(request)
