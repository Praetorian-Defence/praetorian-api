from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from apps.core.models.base import BaseModel


class AuthSource(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'auth_sources'
        default_permissions = ('view', 'add', 'delete')
        verbose_name = _('auth_source')
        verbose_name_plural = _('auth_sources')

    class DriverEnum(Enum):
        DB = 'db'
        LDAP = 'ldap'

    class FlavourEnum(Enum):
        AD = 'ad'

    creator = models.ForeignKey(
        'User', null=True, on_delete=models.CASCADE,
        related_name='auth_sources', verbose_name=_('auth_source_creator')
    )
    name = models.CharField(max_length=100, null=False, verbose_name=_('auth_source_name'))
    driver = EnumChoiceField(DriverEnum, null=False, default=DriverEnum.DB, verbose_name=_('auth_source_driver'))
    content = models.JSONField(null=False, default=dict, verbose_name=_('auth_source_content'))
    is_active = models.BooleanField(null=False, default=False, verbose_name=_('auth_source_is_active'))
