from django.core.exceptions import ValidationError
from django_api_forms import Form
from django.forms import fields, ModelChoiceField
from django.utils.translation import gettext_lazy as _

from apps.core.models import Service


class RemoteForms:
    class Basic(Form):
        service = ModelChoiceField(queryset=Service.objects.all(), required=True)
        name = fields.CharField(max_length=128, required=True)
        host = fields.CharField(max_length=30, required=True)
        port = fields.CharField(max_length=8, required=False)

        def clean_name(self):
            if ' ' in self.cleaned_data['name']:
                raise ValidationError(_('Remote name cannot contain spaces.'))
            return self.cleaned_data['name']
