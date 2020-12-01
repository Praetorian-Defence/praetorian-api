from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.service import ServiceSerializer


class RemoteSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        host: str
        port: str = None
        services: List[ServiceSerializer.Base] = []
