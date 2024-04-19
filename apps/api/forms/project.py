from django_api_forms import Form
from django.forms import fields


class ProjectForms:
    class Basic(Form):
        name = fields.CharField(max_length=128, required=True)
        is_vpn = fields.BooleanField(required=False)
