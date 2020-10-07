from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class Project(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'projects'
        default_permissions = ()
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    name = models.CharField(max_length=50, null=False, verbose_name=_('project_name'))
    is_vpn = models.BooleanField(null=False, default=False, verbose_name=_('project_is_vpn'))
    remotes = models.ManyToManyField('Remote', related_name='projects', verbose_name=_('projects_remotes'))
