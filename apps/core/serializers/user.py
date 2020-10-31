import datetime
from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.models import User
from apps.core.serializers.language import LanguageSerializer
from apps.core.serializers.user_project import UserProjectSerializer


class RelatedDevice(Serializer):
    id: UUID
    name: str
    certificate: str
    user_projects: List[UserProjectSerializer.Base] = None


class UserSerializer:
    class Base(Serializer):
        id: UUID
        username: str
        name: str
        surname: str
        email: str
        phone: str = None

    class Temporary(Serializer):
        id: UUID
        username: str
        password: str

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
