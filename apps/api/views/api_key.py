import logging
from http import HTTPStatus

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

from apps.api.auth.decorators import superuser_required
from apps.api.errors import ValidationException, ApiException
from apps.api.filters.api_key import ApiKeyFilter
from apps.api.forms.api_key import ApiKeyForms
from apps.api.response import SingleResponse, PaginationResponse
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
        form.populate(api_key)
        api_key.save()

        logging.getLogger('logger').info(
            _('New api key was created by superuser: {user_name}.'.format(
                user_name=request.user.username
            )),
            extra={
                'status_code': HTTPStatus.CREATED,
                'request_body': None,
                'username': request.user.username
            }
        )

        return SingleResponse(request, api_key, status=HTTPStatus.CREATED, serializer=ApiKeySerializer.Base)

    @method_decorator(superuser_required)
    def get(self, request):
        api_keys = ApiKeyFilter(request.GET, queryset=ApiKey.objects.all(), request=request).qs

        return PaginationResponse(request, api_keys, serializer=ApiKeySerializer.Base)


class ApiKeyDetail(View):
    @method_decorator(superuser_required)
    def get(self, request, api_key_id):
        try:
            api_key = ApiKey.objects.get(pk=api_key_id)
        except ApiKey.DoesNotExist:
            raise ApiException(request, _('Api key does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        return SingleResponse(request, api_key, serializer=ApiKeySerializer.Base)

    @transaction.atomic
    @method_decorator(superuser_required)
    def put(self, request, api_key_id):
        try:
            api_key = ApiKey.objects.get(pk=api_key_id)
        except ApiKey.DoesNotExist:
            raise ApiException(request, _('Api key does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        form = ApiKeyForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        form.populate(api_key)
        api_key.save()

        return SingleResponse(request, data=api_key, status=HTTPStatus.OK, serializer=ApiKeySerializer.Base)

    @transaction.atomic
    @method_decorator(superuser_required)
    def delete(self, request, api_key_id):
        try:
            api_key = ApiKey.objects.get(pk=api_key_id)
        except ApiKey.DoesNotExist:
            raise ApiException(request, _('Api key does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        api_key.delete()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
