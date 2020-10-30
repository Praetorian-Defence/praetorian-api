from camel_spitter.models import BaseLogModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.fields.aes_json_field import AesJSONField


class LogEntry(BaseLogModel):
    class Meta:
        app_label = 'core'
        db_table = 'log_entries'
        default_permissions = ()

    status_code = models.IntegerField(null=True, verbose_name=_('log_entry_status_code'))
    request_body = AesJSONField(null=True, verbose_name=_('log_entry_request_body'))
    username = models.CharField(max_length=100, null=True, verbose_name=_('log_entry_username'))
