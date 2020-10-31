from http import HTTPStatus

from django.contrib import auth
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.api.errors import ApiException
from apps.api.response import ErrorResponse
from apps.core.models import Token


class TokenMiddleware(object):
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

        return self.get_response(request)
