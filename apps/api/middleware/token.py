from http import HTTPStatus

from django.contrib import auth
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.api.errors import ApiException
from apps.api.response import ErrorResponse
from apps.core.models import Token, Device


class TokenMiddleware(object):
    @staticmethod
    def _get_logged_device(user, request) -> Device:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        logged_device = None
        devices = user.my_devices.all()

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        for device in devices:
            if device.ip_address == ip_address:
                logged_device = device

        return logged_device

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization', b'').split()

        if not auth_header:
            return self.get_response(request)

        if len(auth_header) != 2:
            return ErrorResponse.create_from_exception(
                ApiException(request, _("Improperly formatted token"), status_code=HTTPStatus.BAD_REQUEST)
            )

        try:
            Token.objects.filter(expires_at__lt=timezone.now()).hard_delete()
        except AttributeError:
            pass

        try:
            user = auth.authenticate(request, token=auth_header[1])
        except ApiException:
            user = None

        if user:
            request.user = user
            request.token = user.tokens.get(pk=auth_header[1])

            logged_device = self._get_logged_device(user, request)

            if logged_device is not None:
                request.logged_device = logged_device
            else:
                raise ApiException(
                    request, _('You are trying to connect from a unknown device.'),
                    status_code=HTTPStatus.FORBIDDEN
                )

        return self.get_response(request)
