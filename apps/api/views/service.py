from http import HTTPStatus

from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException
from apps.api.forms.service import ServiceForms
from apps.api.response import SingleResponse
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
