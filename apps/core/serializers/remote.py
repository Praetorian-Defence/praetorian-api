from uuid import UUID

from porcupine.base import Serializer


class RemoteSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        host: str
        port: str = None
