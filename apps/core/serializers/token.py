import uuid

from porcupine.base import Serializer


class TokenSerializer:
    class Base(Serializer):
        token: uuid.UUID
        active_2fa: bool

        @staticmethod
        def resolve_token(token):
            return token.pk
