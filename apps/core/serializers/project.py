from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.remote import RemoteSerializer


class ProjectSerializer:
    class Base(Serializer):
        id: UUID
        name: str
        is_vpn: bool
        remotes: List[RemoteSerializer.Base] = None
