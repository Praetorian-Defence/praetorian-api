from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.core.models.base import BaseModel


class UserProjectDevice(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'users_projects_devices'
        default_permissions = ()
        verbose_name = _('users_projects_devices')
        verbose_name_plural = _('users_projects_devices')

    user = models.ForeignKey(
        'User', null=False, on_delete=models.CASCADE, related_name='projects_devices', verbose_name=_('users')
    )
    project = models.ForeignKey(
        'Project', null=False, on_delete=models.CASCADE, related_name='users_devices', verbose_name=_('projects')
    )
    device = models.ForeignKey(
        'Device', null=False, on_delete=models.CASCADE, related_name='user_projects', verbose_name=_('devices')
    )
