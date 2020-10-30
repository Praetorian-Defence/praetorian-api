from django_api_forms import Form
from django.forms import fields, ModelChoiceField

from apps.core.models import Service


class RemoteForms:
    class Basic(Form):
        service = ModelChoiceField(queryset=Service.objects.all(), required=True)
        name = fields.CharField(max_length=128, required=True)
        host = fields.CharField(max_length=30, required=True)
        port = fields.CharField(max_length=8, required=False)
