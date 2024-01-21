from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.device import DeviceSerializer
from apps.core.serializers.remote import RemoteSerializer
from apps.core.serializers.user import UserSerializer


class LogSerializer:
    class Base(Serializer):
        id: UUID
        remote_id: UUID
        user_id: UUID
        device_id: UUID
        cleaned_log: dict = None

    class Detail(Base):
        remote: RemoteSerializer.Base
        user: UserSerializer.Base
        device: DeviceSerializer.Base
