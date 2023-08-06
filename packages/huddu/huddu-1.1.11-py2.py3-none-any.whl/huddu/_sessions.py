import json

import requests

from ._exceptions import APIException


class Session:
    def __init__(self, headers: dict, base_url: str):
        self.headers = headers
        self.base_url = base_url

    def request(
            self, method: str, path: str, params: dict = None, data: dict = None
    ) -> dict:

        if data:
            res = requests.request(
                method,
                f"{self.base_url}{path}",
                data=json.dumps(data),
                headers=self.headers,
            )
        else:
            res = requests.request(
                method, f"{self.base_url}{path}", params=params, headers=self.headers
            )

        if res and res.status_code > 299:
            raise APIException(res.json())
        return res.json()
