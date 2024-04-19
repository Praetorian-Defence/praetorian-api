import random
import string
import uuid
from http import HTTPStatus

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.formats import date_format
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from rolepermissions.roles import assign_role

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.forms.temporary_user import TemporaryUserForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse
from apps.core.models import User, Language, Device, UserProjectDevice, AuthSource
from apps.core.services.notification import NotificationService


def get_random_email(length):
    name = ''.join(random.choice(string.ascii_letters) for x in range(length))
    return name + '@praetorian.sk'


@transaction.atomic
@token_required
@permission_required('core.add_temporary_user')
@require_http_methods(['POST'])
def create_temporary_user(request):
    form = TemporaryUserForms.Create.create_from_request(request)
    device = request.logged_device

    if not form.is_valid():
        raise ValidationException(request, form)

    project = form.cleaned_data['project_id']
    remote = form.cleaned_data['remote_id']

    try:
        UserProjectDevice.objects.get(user=request.user, project=project, device=device)
    except UserProjectDevice.DoesNotExist:
        raise ApiException(
            request, _('Specified project does not belong to the user.'), status_code=HTTPStatus.NOT_FOUND
        )
    if remote not in project.remotes.all():
        raise ApiException(
            request, _('Specified remote does not belong to the specified project.'), status_code=HTTPStatus.NOT_FOUND
        )

    email = get_random_email(7)

    temporary_user = User.objects.create(
        username=email,
        email=email,
        name='temp_user',
        surname='temp_user',
        is_temporary=True,
        is_active=True,
        auth_source=AuthSource.objects.get(driver=AuthSource.DriverEnum.DB),
        active_to=timezone.now() + settings.TEMPORARY_USER_EXPIRATION,
        language=Language.objects.get(code='sk'),
        creator=request.user,
    )

    password = User.objects.make_random_password()
    temporary_user.set_password(password)
    temporary_user.additional_data = {'remote_id': str(remote.id)}
    assign_role(temporary_user, 'temporary')
    temporary_user.save()

    device = Device.objects.create(
        user=temporary_user,
        name=f'temporary_{email}',
        certificate=uuid.uuid4(),
        ip_address=device.ip_address
    )

    UserProjectDevice.objects.create(user=temporary_user, project=project, device=device)

    NotificationService.create(
        recipients=[request.user.email],
        sender=f'{settings.EMAIL_SENDER_NAME} <{settings.EMAIL_SENDER}>',
        subject=_('[Praetorian API] - Temporary user activation'),
        content={
            'message': _(
                'test'
            ),
            'username': temporary_user.username,
            'password': password,
            'email_text': _(
                'Your temporary user is successfully activated to {expiration}. Credentials are listed below:'
            ).format(expiration=date_format(temporary_user.active_to, format='SHORT_DATE_FORMAT', use_l10n=True)),
        },
        template='_emails/temporary_user_activation.html'
    ).send_email()

    # variables = VariablesService.create(request=request, variables=remote.variables).get_variables()

    response = {
        'username': temporary_user.username,
        'password': password,
        'variables': remote.variables
    }

    return SingleResponse(
        request, response, status=HTTPStatus.CREATED
    )
