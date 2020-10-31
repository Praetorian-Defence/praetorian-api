from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class PasswordRecovery(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'password_recoveries'
        default_permissions = ()

    user = models.ForeignKey(
        'User',
        null=False,
        on_delete=models.CASCADE,
        related_name='password_recoveries',
        verbose_name=_('password_recovery_user')
    )
    value = models.CharField(max_length=200, null=False, verbose_name=_('password_recovery_value'))
    expires_at = models.DateTimeField(null=False, blank=True, verbose_name=_('password_recovery_expires_at'))
