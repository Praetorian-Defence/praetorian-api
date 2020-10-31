import json

from django.conf import settings

from apps.api.auth.aes_encryptor import AesEncryptor
from apps.core.fields.aes_text_field import AesTextField


class AesJSONField(AesTextField):
    # when getting data from DB
    def from_db_value(self, value, expression, connection):
        if value:
            decrypted_data = json.loads(
                AesEncryptor.create_from_secret(settings.AES_SECRET.encode(), self._aes_mode).decrypt(value)
            )
        else:
            decrypted_data = None
        return decrypted_data

    # When deserializing and clean data
    def to_python(self, value):
        if value:
            value = value.replace('\'', '"')
        return value

    # when saving data to DB
    def get_prep_value(self, value):
        if value is None:
            return value
        if not isinstance(value, str):
            value = json.dumps(value)
        return AesEncryptor.create_from_secret(settings.AES_SECRET.encode(), self._aes_mode).encrypt(value)
