from django_api_forms import Form, EnumField
from django.forms import fields

from apps.core.models import ApiKey


class ApiKeyForms:
    class Basic(Form):
        name = fields.CharField(max_length=100, required=True)
        type = EnumField(enum=ApiKey.ApiKeyType, required=True)
        key = fields.CharField(max_length=100, required=True)
        secret = fields.CharField(max_length=100, required=True)
        is_active = fields.BooleanField(required=False)
