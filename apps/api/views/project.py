from http import HTTPStatus

from django.db import transaction
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _
from object_checker.base_object_checker import has_object_permission

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException, ApiException
from apps.api.filters.project import ProjectFilter
from apps.api.forms.project import ProjectForms
from apps.api.permissions import permission_required
from apps.api.response import SingleResponse, PaginationResponse
from apps.core.models import Project
from apps.core.serializers.project import ProjectSerializer


class ProjectManagement(View):
    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_project'))
    def post(self, request):
        form = ProjectForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        project = Project()
        form.populate(project)
        project.save()

        return SingleResponse(request, project, status=HTTPStatus.CREATED, serializer=ProjectSerializer.Detail)

    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_project'))
    def get(self, request):
        projects = ProjectFilter(request.GET, queryset=Project.objects.all(), request=request).qs

        return PaginationResponse(request, projects, serializer=ProjectSerializer.Base)


class ProjectDetail(View):
    @method_decorator(token_required)
    @method_decorator(permission_required('core.read_project'))
    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise ApiException(request, _('Project does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        if not has_object_permission('check_project', request.user, project):
            raise ApiException(request, _('User is unauthorized.'), status_code=HTTPStatus.FORBIDDEN)

        return SingleResponse(request, project, serializer=ProjectSerializer.Detail)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.add_project'))
    def put(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise ApiException(request, _('Project does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        form = ProjectForms.Basic.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        form.populate(project)
        project.save()

        return SingleResponse(request, data=project, status=HTTPStatus.OK, serializer=ProjectSerializer.Detail)

    @transaction.atomic
    @method_decorator(token_required)
    @method_decorator(permission_required('core.delete_project'))
    def delete(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise ApiException(request, _('Project does not exist.'), status_code=HTTPStatus.NOT_FOUND)

        for remote in project.remotes.all():
            remote.services.all().delete()
            remote.delete()
        project.delete()

        return HttpResponse(status=HTTPStatus.NO_CONTENT)
