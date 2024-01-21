from django.conf import settings
from django.db import models

from apps.api.auth.aes_encryptor import AesEncryptor


class AesTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self._aes_mode = kwargs.get('mode')
        if self._aes_mode:
            kwargs.pop('mode')
        else:
            self._aes_mode = 'cfb'

        super(AesTextField, self).__init__(*args, **kwargs)

    # when getting data from DB
    def from_db_value(self, value, expression, connection):
        if value:
            decrypted_data = AesEncryptor.create_from_secret(
                settings.AES_SECRET.encode(), self._aes_mode
            ).decrypt(value)
        else:
            decrypted_data = None
        return decrypted_data

    # When deserializing and clean data
    def to_python(self, value):
        return value

    # when saving data to DB
    def get_prep_value(self, value):
        if not value:
            return value
        if not isinstance(value, str):
            value = str(value)
        return AesEncryptor.create_from_secret(settings.AES_SECRET.encode(), self._aes_mode).encrypt(value)
