from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class AuditLog(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'audit_logs'
        default_permissions = ()
        verbose_name = _('audit_logs')
        verbose_name_plural = _('audit_logs')

    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='logs', verbose_name=_('audit_log_user')
    )
    remote = models.ForeignKey(
        'Remote', on_delete=models.CASCADE, related_name='logs', verbose_name=_('audit_log_remote')
    )
    device = models.ForeignKey(
        'Device', on_delete=models.CASCADE, related_name='logs', verbose_name=_('audit_log_device')
    )
    base_log = models.JSONField(null=True, default=dict, verbose_name=_('audit_log_base_log'))
    cleaned_log = models.JSONField(default=dict, verbose_name=_('audit_log_cleaned_log'))
