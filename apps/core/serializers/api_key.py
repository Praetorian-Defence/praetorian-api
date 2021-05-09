from uuid import UUID

from porcupine.base import Serializer

from apps.core.models import ApiKey


class ApiKeySerializer:
    class Base(Serializer):
        id: UUID
        name: str
        type: ApiKey.ApiKeyType
        key: str
        secret: str
        is_active: bool
