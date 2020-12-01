from django.core.exceptions import ValidationError
from django_api_forms import Form, EnumField, AnyField
from django.forms import fields
from django.utils.translation import gettext_lazy as _

from apps.core.models import Service


class ServiceForms:
    class Basic(Form):
        name = fields.CharField(max_length=100, required=True)
        type = EnumField(enum=Service.ServiceType, required=True)
        variables = AnyField(required=False)

        def clean_name(self):
            if ' ' in self.cleaned_data['name']:
                raise ValidationError(_('Service name cannot contain spaces.'))
            return self.cleaned_data['name']
