from datetime import datetime
from uuid import UUID

from porcupine.base import Serializer


class PasswordRecoverySerializer:
    class Base(Serializer):
        id: UUID
        user_id: UUID
        value: str
        expires_at: datetime
