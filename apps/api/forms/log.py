from django_api_forms import Form
from django.forms import ModelChoiceField, fields

from apps.core.models import Remote, Device


class LogForms:
    class Create(Form):
        base_log =  fields.JSONField(required=True)
        remote_id = ModelChoiceField(queryset=Remote.objects.all(), required=True)
