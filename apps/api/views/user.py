import base64
from datetime import datetime

from io import BytesIO
from http import HTTPStatus

import pyotp
import qrcode
import six
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.decorators import method_decorator
from django.utils.http import int_to_base36
from django.views import View
from django.utils.translation import gettext_lazy as _
from rolepermissions.roles import assign_role, clear_roles

from apps.api.auth.ldap_backend import LDAPService
from apps.api.filters.user import UserFilter
from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException, ActiveDirectoryManagerException
from apps.api.forms.password import PasswordActivateForm
from apps.api.forms.user import UserForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import User, AuthSource
from apps.core.models.password_recovery import PasswordRecovery
from apps.core.serializers.password import PasswordRecoverySerializer
from apps.core.serializers.user import UserSerializer
from apps.core.services.notification import NotificationService


class UserProfile(View):
    @method_decorator(token_required)
    def get(self, request):
        return SingleResponse(request, request.user, serializer=UserSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    def delete(self, request):
        user = request.user

        if user.is_temporary:
            user.delete()
        else:
            raise ApiException(request, _('Permission denied.'), status_code=HTTPStatus.FORBIDDEN)

        return HttpResponse(status=HTTPStatus.NO_CONTENT)


class UserManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_user'))
    def post(self, request):
        form = UserForms.Create.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        password = form.cleaned_data.get('password')
        role = form.cleaned_data.get('role')

        user = User()
        form.fill(user)

        user.set_password(password)
        user.username = user.email
        assign_role(user, role.name)
        user.is_active = False
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

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_user'))
    def put(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ApiException(request, _('User does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        form = UserForms.Update.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        email = form.cleaned_data.get('email')
        assign_projects = form.cleaned_data.get('assign_projects')
        role = form.cleaned_data.get('role')

        if email != user.email:
            if User.objects.filter(email=email).exists():
                raise ApiException(request, _('Email is already used.'), status_code=HTTPStatus.CONFLICT)

        form.fill(user)
        user.username = email
        if assign_projects is not None:
            user.assign_projects(request, assign_projects)
        if role:
            clear_roles(user)
            assign_role(user, role.value)
        user.save()

        return SingleResponse(request, data=user, status=HTTPStatus.OK, serializer=UserSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.delete_user'))
    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ApiException(request, _('User does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        user.delete()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)


class User2faActivate(View):
    @method_decorator(token_required)
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


class PasswordRecoveryManagement(View):
    @transaction.atomic
    def get(self, request, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ApiException(
                request, _('User with specified email does not exist.'), status_code=HTTPStatus.NOT_FOUND
            )

        timestamp = int(datetime.utcnow().timestamp())
        ts_b36 = int_to_base36(timestamp)
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        hash_value = six.text_type(user.pk) + user.password + six.text_type(login_timestamp) + six.text_type(timestamp)

        recovery_hash = salted_hmac(
            settings.SECRET_KEY,
            hash_value,
        ).hexdigest()[::2]

        password_recovery = PasswordRecovery.objects.create(
            value="%s-%s" % (ts_b36, recovery_hash),
            user=user,
            expires_at=timezone.now() + settings.PASSWORD_RECOVERY_TIME
        )

        recovery_url = f'{settings.BASE_URL}/password/activate/{password_recovery.value}'

        NotificationService.create(
            recipients=[user.email],
            sender=f"{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_SENDER}>",
            subject=_('[Praetorian API] - Email recovery'),
            content={
                'message': _(
                    'test'
                ),
                'recovery_url': recovery_url,
                'email_text': _('Your recovery link to Praetorian API is: ')
            },
            template='_emails/password_recovery.html'
        ).send_email()

        return SingleResponse(
            request, password_recovery, status=HTTPStatus.CREATED, serializer=PasswordRecoverySerializer.Base
        )


class PasswordActivateManagement(View):
    @transaction.atomic
    def post(self, request):
        form = PasswordActivateForm.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        request_data = form.cleaned_data

        try:
            password_recovery = PasswordRecovery.objects.get(
                value=request_data.get('hashed_recovery'),
                expires_at__gt=timezone.now()
            )
        except PasswordRecovery.DoesNotExist:
            raise ApiException(request, _('Password recovery does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        password_recovery.user.set_password(request_data.get('password'))
        password_recovery.user.save()
        PasswordRecovery.objects.filter(user=password_recovery.user).delete()

        return SingleResponse(request, None, status=HTTPStatus.NO_CONTENT)


class UserActiveDirectoryDetail(View):
    @method_decorator(token_required)
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ApiException(request, _('User does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        if user.auth_source.driver == AuthSource.DriverEnum.LDAP:
            try:
                user = LDAPService(user).get_user()
            except ActiveDirectoryManagerException:
                raise ApiException(request, _('LDAP error!'), status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        else:
            raise ApiException(
                request, _('User is not member of active directory!'), status_code=HTTPStatus.CONFLICT
            )

        return SingleResponse(request, user)
