from http import HTTPStatus

import pyotp
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.api.forms.auth import AuthUserForm, Auth2faForm
from apps.api.response import SingleResponse
from apps.api.errors import ValidationException, ApiException
from apps.core.models import Token
from apps.core.serializers.token import TokenSerializer


class AuthUser(View):
    def post(self, request):
        form = AuthUserForm.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        data = form.cleaned_data

        user = authenticate(request, username=data.get('username'), password=data.get('password'))

        if user is None:
            raise ApiException(request, _('Incorrect username or password'), HTTPStatus.UNAUTHORIZED)

        expires_at = timezone.now() + settings.TOKEN_EXPIRATION

        token = Token.objects.create(
            user_id=user.pk,
            expires_at=expires_at
        )

        return SingleResponse(request, token, status=HTTPStatus.OK, serializer=TokenSerializer.Base)


class Auth2fa(View):
    def post(self, request):
        form = Auth2faForm.Basic.create_from_request(request)

        if not request.token:
            raise ApiException(request, _('User is unauthorized.'), status_code=HTTPStatus.FORBIDDEN)

        if not form.is_valid():
            raise ValidationException(request, form)

        code = form.cleaned_data.get('code')
        user = request.user
        token = request.token

        if user.is_2fa:
            totp = pyotp.TOTP(user.additional_data.get('otp_secret'))
            totp.now()

            if totp.verify(code):
                token.active_2fa = True
                token.save()
            else:
                raise ApiException(request, _('Invalid or missing credentials'), status_code=HTTPStatus.UNAUTHORIZED)
        else:
            raise ApiException(request, _('User is unauthorized.'), status_code=HTTPStatus.FORBIDDEN)

        return SingleResponse(request, token, status=HTTPStatus.OK, serializer=TokenSerializer.Base)
