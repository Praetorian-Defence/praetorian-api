from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel
from apps.core.fields.aes_text_field import AesTextField


class Device(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'devices'
        default_permissions = ()
        verbose_name = _('device')
        verbose_name_plural = _('devices')

    name = models.CharField(max_length=50, null=False, verbose_name=_('device_name'))
    certificate = AesTextField(max_length=50, null=False, verbose_name=_('device_certificate'))
