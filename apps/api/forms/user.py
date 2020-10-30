from django.core.exceptions import ValidationError
from django.forms import fields, ModelChoiceField
from django_api_forms import Form, AnyField, BooleanField, EnumField
from django.utils.translation import gettext_lazy as _

from apps.core.models import User, Language


class UserForms:
    class Basic(Form):
        username = fields.CharField(required=True)
        password = fields.CharField(required=True)
        name = fields.CharField(required=True)
        surname = fields.CharField(required=True)
        email = fields.EmailField(required=True)
        phone = fields.CharField(required=True)

        is_temporary = BooleanField(required=True)
        is_vpn = BooleanField(required=False)

        source = EnumField(enum=User.Source, required=True)
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
