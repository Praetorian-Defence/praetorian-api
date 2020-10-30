from uuid import UUID

from porcupine.base import Serializer


class LanguageSerializer:
    class Base(Serializer):
        id: UUID
        code: str
        name: str
        bundle: str
