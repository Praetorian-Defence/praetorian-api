from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.user_project import UserProjectSerializer


class DeviceSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        certificate: str
        user_projects: List[UserProjectSerializer.Base] = None
