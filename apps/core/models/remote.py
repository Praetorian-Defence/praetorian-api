from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.fields.aes_json_field import AesJSONField
from apps.core.models.base import BaseModel
from apps.core.fields.aes_text_field import AesTextField


class Remote(BaseModel):
    class Meta:
        app_label = 'core'
        db_table = 'remotes'
        default_permissions = ()
        verbose_name = _('remote')
        verbose_name_plural = _('remotes')

    name = models.CharField(max_length=100, null=False, verbose_name=_('remote_name'))
    host = AesTextField(null=False, verbose_name=_('remote_host'))
    port = AesTextField(null=False, verbose_name=_('remote_port'))
    user = AesTextField(null=False, verbose_name=_('remote_user'))
    password = AesTextField(null=False, verbose_name=_('remote_password'))
    variables = AesJSONField(null=False, default=dict, verbose_name=_('remote_variables'))

    project = models.ForeignKey(
        'Project', null=False, on_delete=models.CASCADE, related_name='remotes', verbose_name=_('remote_project')
    )

    def validate_unique(self, exclude=None):
        qs = Remote.objects.filter(name=self.name)
        if qs.filter(project__pk=self.project_id).exists():
            raise ValidationError(_('Remote name must be unique per project.'))

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Remote, self).save(*args, **kwargs)
