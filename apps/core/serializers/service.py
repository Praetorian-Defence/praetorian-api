from uuid import UUID

from porcupine.base import Serializer

from apps.core.models import Service


class ServiceSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        type: Service.ServiceType
