from http import HTTPStatus

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _
from object_checker.base_object_checker import has_object_permission

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.filters.remote import RemoteFilter
from apps.api.forms.remote import RemoteForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse, PaginationResponse
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

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_remote'))
    def get(self, request):
        remotes = RemoteFilter(request.GET, queryset=Remote.objects.all(), request=request).qs

        return PaginationResponse(request, remotes, serializer=RemoteSerializer.Base)


class RemoteDetail(View):
    @method_decorator(token_required)
    @method_decorator(permission_required('read_remote'))
    def get(self, request, remote_id):
        try:
            remote = Remote.objects.get(pk=remote_id)
        except Remote.DoesNotExist:
            raise ApiException(request, _('Remote does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        if not has_object_permission('check_remote', request.user, remote):
            raise ApiException(request, _('User is unauthorized.'), status_code=HTTPStatus.FORBIDDEN)

        return SingleResponse(request, remote, serializer=RemoteSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_remote'))
    def put(self, request, remote_id):
        try:
            remote = Remote.objects.get(pk=remote_id)
        except Remote.DoesNotExist:
            raise ApiException(request, _('Remote does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        form = RemoteForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        form.fill(remote)
        remote.save()

        return SingleResponse(request, data=remote, status=HTTPStatus.OK, serializer=RemoteSerializer.Base)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.delete_remote'))
    def delete(self, request, remote_id):
        try:
            remote = Remote.objects.get(pk=remote_id)
        except Remote.DoesNotExist:
            raise ApiException(request, _('Remote does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        remote.delete()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
