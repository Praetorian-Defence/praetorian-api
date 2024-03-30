from enum import Enum

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class AuthSourceGroup(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'auth_source_groups'
        default_permissions = ()
        verbose_name = _('auth_source_group')
        verbose_name_plural = _('auth_source_groups')

    class DriverEnum(Enum):
        DB = 'db'
        LDAP = 'ldap'

    auth_source = models.ForeignKey('AuthSource', null=True, on_delete=models.CASCADE, related_name='groups')
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name='sources')
    external = models.CharField(max_length=200, null=True, verbose_name=_('auth_source_group_external'))
