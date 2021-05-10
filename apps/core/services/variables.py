from http import HTTPStatus

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.api.errors import ApiException
from apps.core.models import ApiKey


class VariablesService(object):
    def __init__(
        self,
        request: HttpRequest,
        variables: dict
    ):
        self._request = request
        self._variables = variables

        if hasattr(self._request, 'api_key'):
            self._api_key = self._request.api_key
        else:
            raise ApiException(
                self._request, _('Request does not have any api_key.'), status_code=HTTPStatus.NOT_FOUND
            )

    @classmethod
    def create(
        cls,
        request: HttpRequest,
        variables: dict
    ) -> 'VariablesService':
        return VariablesService(request, variables)

    def get_variables(self) -> dict:
        variables = {}

        if self._api_key.type == ApiKey.ApiKeyType.PROXY_CLIENT:
            variables = self._get_all_variables(self._variables)
        elif self._api_key.type == ApiKey.ApiKeyType.USER_CLIENT or ApiKey.ApiKeyType.DEBUG:
            variables = self._get_public_variables(self._variables)

        return variables

    def _get_all_variables(self, variables: dict):
        dictionary = {}

        for k, v in variables.items():
            if isinstance(v['value'], dict):
                dictionary[k] = self._get_all_variables(v['value'])
            else:
                dictionary[k] = v['value']

        return dictionary

    def _get_public_variables(self, variables: dict):
        dictionary = {}

        for k, v in variables.items():
            if isinstance(v['value'], dict):
                if v['hidden']:
                    dictionary[k] = None
                else:
                    dictionary[k] = self._get_public_variables(v['value'])
            else:
                if v['hidden']:
                    dictionary[k] = None
                else:
                    dictionary[k] = v['value']

        return dictionary
