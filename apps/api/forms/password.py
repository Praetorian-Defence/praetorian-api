from django.forms import fields
from django_api_forms import Form, BooleanField


class PasswordRecoveryForm(Form):
    email = fields.EmailField(required=True)


class PasswordActivateForm(Form):
    password = fields.CharField(max_length=32, required=True)
    hashed_recovery = fields.CharField(required=True)
