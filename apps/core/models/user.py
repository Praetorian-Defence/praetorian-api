from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from apps.core.managers.user import UserManager
from apps.core.models.base import BaseModel
from apps.core.fields.aes_text_field import AesTextField


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = 'core'
        db_table = 'users'
        default_permissions = ()
        verbose_name = _('user')
        verbose_name_plural = _('users')

    class Source(Enum):
        LDAP = 'ldap'
        DB = 'db'

    username = models.CharField(max_length=255, unique=True, verbose_name=_('username'))
    name = models.CharField(max_length=100, verbose_name=_('user_name'))
    surname = models.CharField(max_length=100, verbose_name=_('user_surname'))
    email = models.CharField(max_length=255, unique=True, verbose_name=_('user_email'))
    is_active = models.BooleanField(default=False, verbose_name=_('user_is_active'))
    is_vpn = models.BooleanField(default=False, verbose_name=_('user_is_vpn'))
    is_2fa = models.BooleanField(default=False, verbose_name=_('user_is_2fa'))
    is_temporary = models.BooleanField(default=False, verbose_name=_('user_is_temporary'))
    source = EnumChoiceField(Source, null=False, default=Source.DB, verbose_name=_('user_source'))
    phone = AesTextField(null=True, verbose_name=_('user_phone'))
    additional_data = models.JSONField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'surname']

    def get_full_name(self) -> str:
        return f'{self.name} {self.surname}'

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email
