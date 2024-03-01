import importlib
from typing import List
from uuid import UUID

from porcupine.base import Serializer

from apps.core.serializers.service import ServiceSerializer
from apps.core.services.variables import VariablesService


class RemoteSerializer:
    class Base(Serializer):
        id: UUID
        project_id: UUID
        name: str
        host: str
        port: str
        user: str
        password: str
        variables: dict = {}
        project: dict = {}
        services: List[ServiceSerializer.Base] = []

        @staticmethod
        def resolve_project(data, **kwargs) -> dict:
            project = data.project

            project_serializer = getattr(importlib.import_module('apps.core.serializers.project'), 'ProjectSerializer')
            serialized_project = project_serializer.Base(project).dict()

            return serialized_project

        # @staticmethod
        # def resolve_variables(data, **kwargs) -> dict:
        #     request = kwargs['request']
        #
        #     return VariablesService.create(request=request, variables=data.variables).get_variables()
#
