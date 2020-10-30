import datetime
from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.models import User
from apps.core.serializers.language import LanguageSerializer


class RelatedDevice(Serializer):
    id: UUID
    name: str
    certificate: str


class UserSerializer:
    class Base(Serializer):
        id: UUID
        username: str
        name: str
        surname: str
        email: str
        phone: str = None

    class Detail(Serializer):
        id: UUID
        username: str
        name: str
        surname: str
        email: str
        phone: str = None

        is_active: bool
        is_vpn: bool
        is_2fa: bool
        is_temporary: bool

        source: User.Source
        additional_data: dict = None
        active_to: datetime.datetime = None

        language: LanguageSerializer.Base
        my_devices: List[RelatedDevice] = None
