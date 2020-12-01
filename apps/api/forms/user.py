from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import fields, ModelChoiceField, ModelMultipleChoiceField
from django_api_forms import Form, AnyField, BooleanField, EnumField, FormFieldList
from django.utils.translation import gettext_lazy as _

from apps.core.models import User, Language, Project, Device


class AssignProjectsForm(Form):
    project_id = ModelChoiceField(queryset=Project.objects.all(), required=True)
    devices = ModelMultipleChoiceField(queryset=Device.objects.all(), required=True)


class UserForms:
    class Basic(Form):
        email = fields.EmailField(required=True)
        password = fields.CharField(required=True)
        name = fields.CharField(required=True)
        surname = fields.CharField(required=True)
        phone = fields.CharField(required=False)

        is_vpn = BooleanField(required=False)

        source = EnumField(enum=User.Source, required=True)
        role = ModelChoiceField(to_field_name='name', queryset=Group.objects.all(), required=True)
        additional_data = AnyField(required=False)

        language_id = ModelChoiceField(queryset=Language.objects.all(), required=False)

        def clean_username(self):
            if User.objects.filter(username=self.cleaned_data['username']).exists():
                raise ValidationError(_('User with this username already exists!'))
            return self.cleaned_data['username']

        def clean_email(self):
            if User.objects.filter(email=self.cleaned_data['email']).exists():
                raise ValidationError(_('User with this email already exists!'))
            return self.cleaned_data['email']

    class Update(Form):
        email = fields.EmailField(required=True)
        name = fields.CharField(required=True)
        surname = fields.CharField(required=True)
        phone = fields.CharField(required=False)

        is_vpn = BooleanField(required=False)

        source = EnumField(enum=User.Source, required=True)
        role = ModelChoiceField(to_field_name='name', queryset=Group.objects.all(), required=False)
        additional_data = AnyField(required=False)
        assign_projects = FormFieldList(form=AssignProjectsForm, required=False)

        language_id = ModelChoiceField(queryset=Language.objects.all(), required=False)
