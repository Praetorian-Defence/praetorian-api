from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.api.views import project

urlpatterns = [
    path('projects/', project.ProjectManagement.as_view(), name='project-management'),
]
