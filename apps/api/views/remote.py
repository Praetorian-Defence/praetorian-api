from http import HTTPStatus

from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException
from apps.api.forms.remote import RemoteForms
from apps.api.response import SingleResponse
from apps.core.models import Remote
from apps.core.serializers.remote import RemoteSerializer


class RemoteManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_remote'))
    def post(self, request):
        form = RemoteForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        remote = Remote()
        form.fill(remote)
        remote.save()

        return SingleResponse(request, remote, status=HTTPStatus.CREATED, serializer=RemoteSerializer.Base)
