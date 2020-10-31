from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class Token(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'tokens'
        default_permissions = ()

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tokens', verbose_name=_('token_user'))
    active_2fa = models.BooleanField(null=False, default=False, verbose_name=_('token-active-2fa'))
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name=_('token_expires_at'))
