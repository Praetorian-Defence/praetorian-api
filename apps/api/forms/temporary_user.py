from django.forms import ModelChoiceField
from django_api_forms import Form

from apps.core.models import Project, Remote, Service


class TemporaryUserForms:
    class Create(Form):
        project_id = ModelChoiceField(queryset=Project.objects.all(), required=True)
        remote_id = ModelChoiceField(queryset=Remote.objects.all(), required=True)
