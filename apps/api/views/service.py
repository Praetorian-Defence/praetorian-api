from http import HTTPStatus

from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.filters.service import ServiceFilter
from apps.api.forms.service import ServiceForms
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import Service
from apps.core.serializers.service import ServiceSerializer


class ServiceManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_service'))
    def post(self, request):
        form = ServiceForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        service = Service()
        form.fill(service)
        service.save()

        return SingleResponse(request, service, status=HTTPStatus.CREATED, serializer=ServiceSerializer.Base)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_service'))
    def get(self, request):
        services = ServiceFilter(request.GET, queryset=Service.objects.all(), request=request).qs

        return PaginationResponse(request, services, serializer=ServiceSerializer.Base)


class ServiceDetail(View):
    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_service'))
    def get(self, request, service_id):
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ApiException(request, _('Service does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        return SingleResponse(request, service, serializer=ServiceSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_service'))
    def put(self, request, service_id):
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ApiException(request, _('Service does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        form = ServiceForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        form.fill(service)
        service.save()

        return SingleResponse(request, data=service, status=HTTPStatus.OK, serializer=ServiceSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.delete_service'))
    def delete(self, request, service_id):
        try:
            service = Service.objects.get(pk=service_id)
        except Service.DoesNotExist:
            raise ApiException(request, _('Service does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        service.delete()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
