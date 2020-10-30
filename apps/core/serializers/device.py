from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.user import UserSerializer


class DeviceSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        certificate: str
        user: UserSerializer.Base
