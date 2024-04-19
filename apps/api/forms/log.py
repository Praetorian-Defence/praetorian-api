from django_api_forms import Form, AnyField
from django.forms import ModelChoiceField

from apps.core.models import Remote


class AuditLogForms:
    class Create(Form):
        base_log = AnyField(required=True)
        remote_id = ModelChoiceField(queryset=Remote.objects.all(), required=True)
