from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from apps.core.models.base import BaseModel


class ApiKey(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'api_keys'
        default_permissions = ()
        verbose_name = _('api_key')
        verbose_name_plural = _('api_keys')

    class DevicePlatformEnum(Enum):
        IOS = 'ios'
        ANDROID = 'android'
        WEB = 'web'
        EXTERNAL = 'external'

        def __str__(self):
            return _(f"api_key_{self.value}")

    platform = EnumChoiceField(DevicePlatformEnum, null=False, default=DevicePlatformEnum.WEB)
    key = models.CharField(max_length=100, null=False, unique=True)
    secret = models.CharField(max_length=100, null=False)
    is_active = models.BooleanField(null=False, default=False)
