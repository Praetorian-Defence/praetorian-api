from Crypto.Cipher import AES
import base64

from Crypto.Random import get_random_bytes
from django.conf import settings
from django.db import models


class AesTextField(models.TextField):
    secret = settings.AES_SECRET.encode()

    def __init__(self, *args, **kwargs):
        super(AesTextField, self).__init__(*args, **kwargs)

    def encrypt(self, raw):
        raw = base64.b64encode(self._padding(raw).encode())
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(key=self.secret, mode=AES.MODE_CFB, iv=iv)

        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.secret, AES.MODE_CFB, iv)

        return self._unpadding(base64.b64decode(cipher.decrypt(enc[AES.block_size:]))).decode()

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        # when getting data
        return self.decrypt(value)

    def get_prep_value(self, value):
        # when saving data
        if not value:
            return value
        if not isinstance(value, str):
            value = str(value)
        return self.encrypt(value)

    @staticmethod
    def _unpadding(s):
        return s[:-ord(s[-1:])]

    @staticmethod
    def _padding(s):
        block_size = AES.block_size
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
