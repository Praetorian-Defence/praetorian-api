import json
from json import JSONEncoder
from typing import Dict, Union, List
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request
from urllib.parse import urlencode

from apps.api.errors import ApiException


class Requestor:
    def __init__(self, api_url: str, timeout: int = 30):
        self._api_url = api_url
        self._timeout = timeout

    def request(
        self, method: str, endpoint_url: str, payload: dict = None, query: dict = None, parse: bool = True
    ) -> Union[List, Dict]:
        if query and isinstance(query, dict):
            params = urlencode(query)
            endpoint_url += f'?{params}'

        request = Request(
            method=method,
            url=self._api_url + endpoint_url,
            headers={
                'Content-Type': 'application/json'
            }
        )

        if payload and isinstance(payload, dict):
            request.data = json.dumps(payload, cls=JSONEncoder).encode('utf-8')

        try:
            response = urlopen(request, timeout=self._timeout)
        except HTTPError as error:
            raise ApiException(request, f'{error.status} - {error.reason}')
        except URLError as error:
            raise ApiException(request, error.reason)
        else:
            if parse:
                try:
                    data = json.loads(response.read())
                except json.JSONDecodeError:
                    raise ApiException(request, 'Cannot parse the response data to json format.')
            else:
                data = response.read()

            return data
