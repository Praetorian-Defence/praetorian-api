from http import HTTPStatus

from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views import View

from apps.api.auth.decorators import token_required
from apps.api.errors import ValidationException
from apps.api.forms.project import ProjectForms
from apps.api.response import SingleResponse
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
        form.fill(project)
        project.save()

        remotes = form.cleaned_data.get('remotes')
        if remotes:
            for remote in remotes:
                project.remotes.add(remote)

        return SingleResponse(request, project, status=HTTPStatus.CREATED, serializer=ProjectSerializer.Base)
