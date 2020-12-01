from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel
from apps.core.fields.aes_text_field import AesTextField


class Remote(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'remotes'
        default_permissions = ()
        verbose_name = _('remote')
        verbose_name_plural = _('remotes')

    name = models.CharField(max_length=100, unique=True, null=False, verbose_name=_('remote_name'))
    host = AesTextField(null=False, verbose_name=_('remote_host'))
    port = AesTextField(null=True, verbose_name=_('remote_port'))
