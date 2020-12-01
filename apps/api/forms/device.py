from django_api_forms import Form
from django.forms import fields, ModelChoiceField

from apps.core.models import User


class DeviceForms:
    class Basic(Form):
        user = ModelChoiceField(queryset=User.objects.all(), required=True)
        name = fields.CharField(max_length=128, required=True)
        certificate = fields.CharField(max_length=256, required=True)
        ip_address = fields.CharField(max_length=100, required=False)
