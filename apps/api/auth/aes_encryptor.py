import base64
from typing import Union

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AesEncryptor(object):
    def __init__(self, secret: Union[bytes, bytearray, memoryview], mode: str):
        self._secret = secret
        self._mode = mode

    @classmethod
    def create_from_secret(cls, secret: Union[bytes, bytearray, memoryview], mode: str) -> 'AesEncryptor':
        return AesEncryptor(secret, mode)

    def encrypt(self, raw):
        raw = base64.b64encode(self._padding(raw).encode())

        if self._mode == 'cfb':
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key=self._secret, mode=AES.MODE_CFB, iv=iv)

            result = base64.b64encode(iv + cipher.encrypt(raw)).decode()

        else:
            cipher = AES.new(key=self._secret, mode=AES.MODE_SIV)
            ciphertext, tag = cipher.encrypt_and_digest(raw)

            encoded_ciphertext = base64.b64encode(ciphertext).decode()
            encoded_tag = base64.b64encode(tag).decode()

            result = encoded_ciphertext + '|' + encoded_tag

        return result

    def decrypt(self, enc):
        decryption = None

        if enc:
            if self._mode == 'cfb':
                enc = base64.b64decode(enc)
                iv = enc[:AES.block_size]
                cipher = AES.new(self._secret, AES.MODE_CFB, iv)
                decryption = self._unpadding(base64.b64decode(cipher.decrypt(enc[AES.block_size:]))).decode()
            else:
                encoded_ciphertext, encoded_tag = enc.split('|')
                decoded_ciphertext = base64.b64decode(encoded_ciphertext)
                decoded__tag = base64.b64decode(encoded_tag)

                cipher = AES.new(self._secret, AES.MODE_SIV)
                decryption = self._unpadding(cipher.decrypt_and_verify(decoded_ciphertext, decoded__tag))

        return decryption

    @staticmethod
    def _unpadding(s):
        return s[:-ord(s[-1:])]

    @staticmethod
    def _padding(s):
        block_size = AES.block_size
        return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
