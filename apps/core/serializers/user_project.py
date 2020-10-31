import uuid

from porcupine.base import Serializer

from apps.core.serializers.project import ProjectSerializer


class UserProjectSerializer:
    class Base(Serializer):
        user_id: uuid.UUID
        project: ProjectSerializer.Base
