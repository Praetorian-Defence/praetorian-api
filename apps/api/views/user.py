import base64

from io import BytesIO
from http import HTTPStatus

import pyotp
import qrcode
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

from apps.api.filters.user import UserFilter
from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.forms.user import UserForms
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import User
from apps.core.serializers.user import UserSerializer
from apps.core.services.notification import NotificationService


class UserProfile(View):
    @method_decorator(token_required)
    def get(self, request):
        return SingleResponse(request, request.user, serializer=UserSerializer.Detail)


class UserManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_user'))
    def post(self, request):
        form = UserForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        data = form.cleaned_data
        user = User()
        form.fill(user)
        user.set_password(data.get('password'))
        user.save()

        return SingleResponse(request, user, status=HTTPStatus.CREATED, serializer=UserSerializer.Base)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_user'))
    def get(self, request):
        users = UserFilter(request.GET, queryset=User.objects.all(), request=request).qs

        return PaginationResponse(request, users, serializer=UserSerializer.Base)


class UserDetail(View):
    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_user'))
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ApiException(request, _('User does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        return SingleResponse(request, user, serializer=UserSerializer.Detail)


class User2faActivate(View):
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_user'))
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ApiException(request, _('User does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        otp_secret = pyotp.random_base32()
        qr_code_url = pyotp.totp.TOTP(otp_secret).provisioning_uri(
            name=user.email,
            issuer_name="Praetorian API"
        )
        response = {'qr_code': qr_code_url}

        if user.additional_data:
            user.additional_data['otp_secret'] = otp_secret
        else:
            user.additional_data = {'otp_secret': otp_secret}
        user.is_2fa = True
        user.save()

        NotificationService.create(
            recipients=[user.email],
            sender=f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_SENDER}>",
            subject=_('[Praetorian API] - Two factor authentication'),
            content={
                'message': _(
                    'test'
                ),
                'qr_code_url': self.make_qr_code(qr_code_url),
                'email_text': _('QR code to activate your two factor authentication.')
            },
            template='_emails/2fa_activation.html'
        ).send_email()

        return SingleResponse(request, response, status=HTTPStatus.CREATED, serializer=UserSerializer.Base)

    @staticmethod
    def make_qr_code(text):
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image()
        img_buffer = BytesIO()

        img.save(img_buffer, format="PNG")
        img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        return img_str
