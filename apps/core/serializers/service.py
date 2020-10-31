from uuid import UUID

from porcupine.base import Serializer


class ServiceSerializer:
    class Base(Serializer):
        id: UUID
        name: str
