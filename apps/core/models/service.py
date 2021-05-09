from enum import Enum

from django.core.exceptions import ValidationError
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
        POSTGRESQL = 'postgresql'
        MYSQL = 'mysql'
        MARIADB = 'mariadb'
        LDAP = 'ldap'
        REDIS = 'redis'
        SSH = 'ssh'
        ENV = 'env'

    name = models.CharField(max_length=100, unique=True, null=False, verbose_name=_('service_name'))
    type = EnumChoiceField(ServiceType, null=False, default=ServiceType.SSH, verbose_name=_('service_type'))
    variables = AesJSONField(null=False, default=dict, verbose_name=_('service_variables'))

    remote = models.ForeignKey(
        'Remote', null=False, on_delete=models.CASCADE,  related_name='services', verbose_name=_('service_remote')
    )

    def validate_unique(self, exclude=None):
        qs = Service.objects.filter(name=self.name)
        if qs.filter(remote__pk=self.remote_id).exists():
            raise ValidationError(_('Service name must be unique per remote.'))

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Service, self).save(*args, **kwargs)
