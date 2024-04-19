from django.core.exceptions import ValidationError
from django_api_forms import Form, AnyField
from django.forms import fields, ModelChoiceField
from django.utils.translation import gettext_lazy as _

from apps.core.models import Project


class RemoteForms:
    class Basic(Form):
        name = fields.CharField(max_length=128, required=True)
        host = fields.CharField(max_length=30, required=True)
        port = fields.CharField(max_length=8, required=False)
        variables = AnyField(required=False)
        user = fields.CharField()
        password = fields.CharField()

        project_id = ModelChoiceField(queryset=Project.objects.all(), required=True)

        def clean_name(self):
            if ' ' in self.cleaned_data['name']:
                raise ValidationError(_('Remote name cannot contain spaces.'))

            return self.cleaned_data['name']
