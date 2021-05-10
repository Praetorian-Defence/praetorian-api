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
        role: str
        is_temporary: bool
        additional_data: dict = {}

        @staticmethod
        def resolve_role(user, **kwargs) -> str:
            role_name = 'admin'

            if not user.is_superuser:
                role_name = user.groups.first().name

            return role_name

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
        role: str

        is_active: bool
        is_vpn: bool
        is_2fa: bool
        is_temporary: bool

        source: User.Source
        additional_data: dict = {}
        active_to: datetime.datetime = None

        language: LanguageSerializer.Base
        my_devices: List[RelatedDevice] = None

        @staticmethod
        def resolve_role(user, **kwargs) -> str:
            role_name = 'admin'

            if not user.is_superuser:
                role_name = user.groups.first().name

            return role_name
