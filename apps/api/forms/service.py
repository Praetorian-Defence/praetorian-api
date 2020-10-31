from django_api_forms import Form, EnumField, AnyField
from django.forms import fields

from apps.core.models import Service


class ServiceForms:
    class Basic(Form):
        name = fields.CharField(max_length=50, required=True)
        type = EnumField(enum=Service.ServiceType, required=True)
        variables = AnyField(required=False)
