from django_api_forms import Form
from django.forms import fields, ModelMultipleChoiceField

from apps.core.models import Remote


class ProjectForms:
    class Basic(Form):
        name = fields.CharField(max_length=128, required=True)
        is_vpn = fields.BooleanField(required=False)
        remotes = ModelMultipleChoiceField(queryset=Remote.objects.all(), required=False)
