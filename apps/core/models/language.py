from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import BaseModel


class Language(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'languages'
        default_permissions = ()
        verbose_name = _('language')
        verbose_name_plural = _('languages')

    code = models.CharField(max_length=2, null=False, unique=True, verbose_name=_('language_code'))
    name = models.CharField(max_length=50, null=False, verbose_name=_('language_name'))
    bundle = models.CharField(max_length=5, null=False, verbose_name=_('language_bundle'))
