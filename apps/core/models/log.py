from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class Log(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'logs'
        default_permissions = ()
        verbose_name = _('logs')
        verbose_name_plural = _('logs')

    def _upload_to_path(self, filename):
        return f"logs/{self.user.name}/{self.remote.name}/{str(self.pk)}/{filename}"

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='logs', verbose_name=_('log_user')
    )
    remote = models.ForeignKey(
        'Remote', on_delete=models.CASCADE, related_name='logs', verbose_name=_('log_remote')
    )
    device = models.ForeignKey(
        'Device', on_delete=models.CASCADE, related_name='logs', verbose_name=_('log_device')
    )
    base_log = models.JSONField(null=True, default=dict, verbose_name=_('log_log_base'))
    cleaned_log = models.JSONField(default=dict, verbose_name=_('log_log_cleaned'))
