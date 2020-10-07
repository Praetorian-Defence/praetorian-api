from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_enum_choices.fields import EnumChoiceField

from apps.core.models.base import BaseModel
from apps.core.fields.aes_json_field import AesJSONField


class Service(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'services'
        default_permissions = ()
        verbose_name = _('service')
        verbose_name_plural = _('services')

    class ServiceType(Enum):
        DB = 'db'

    name = models.CharField(max_length=50, null=False, verbose_name=_('service_name'))
    type = EnumChoiceField(ServiceType, null=False, default=ServiceType.DB, verbose_name=_('service_type'))
    variables = AesJSONField(null=True, verbose_name=_('service_variables'))
