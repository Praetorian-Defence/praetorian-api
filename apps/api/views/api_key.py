import logging
from http import HTTPStatus

from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

from apps.api.auth.decorators import superuser_required
from apps.api.errors import ValidationException
from apps.api.forms.api_key import ApiKeyForms
from apps.api.response import SingleResponse
from apps.core.models import ApiKey
from apps.core.serializers.api_key import ApiKeySerializer


class ApiKeyManagement(View):
    @transaction.atomic
    @method_decorator(superuser_required)
    def post(self, request):
        form = ApiKeyForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        api_key = ApiKey()
        form.fill(api_key)
        api_key.save()

        logging.getLogger('logger').info(
            _('Vytvorenie nového api kľúča adminom {user_name}.'.format(
                user_name=request.user.username
            )),
            extra={
                'status_code': HTTPStatus.CREATED,
                'request_body': None,
                'username': request.user.username
            }
        )

        return SingleResponse(request, api_key, status=HTTPStatus.CREATED, serializer=ApiKeySerializer.Base)
