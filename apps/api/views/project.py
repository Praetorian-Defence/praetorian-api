from http import HTTPStatus

from django.db import transaction
from django.http import HttpResponse
from django.views import View

from apps.core.models import Service
from apps.core.models import Remote, Project


class ProjectManagement(View):
    @transaction.atomic
    def get(self, request):
        Service.objects.create(
            name='test_service',
            variables={'test': 1}
        )
        service = Service.objects.get(name='test_service')
        print(service.variables)

        # remote = Remote.objects.create(
        #     service=service,
        #     name='test_remote',
        #     host='127.0.0.1',
        #     port='22'
        # )

        # project = Project.objects.create(
        #     name='test_project'
        # )
        # project.remotes.add(remote)
        # project.save()

        # print(project.remotes.all()[0].host)
        # print(project.remotes.all()[0].port)
        # print(project.remotes.all()[0].service.variables)

        return HttpResponse('')
