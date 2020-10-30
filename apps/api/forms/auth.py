from django.forms import fields
from django_api_forms import Form


class AuthUserForm:
    class Basic(Form):
        username = fields.EmailField(required=True)
        password = fields.CharField(max_length=128, required=True)


class Auth2faForm:
    class Basic(Form):
        code = fields.CharField(max_length=30, required=True)
