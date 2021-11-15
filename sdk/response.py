import json
from typing import Dict

from .typing import Header, RawBody


class Response:
    def __init__(self, data: RawBody, status: int, headers: Header) -> None:
        self._raw_data = data
        self._status = status
        self._headers = headers

    @property
    def status(self) -> int:
        return self._status

    @property
    def headers(self) -> Header:
        return self._headers

    @property
    def raw_data(self) -> RawBody:
        return self._raw_data

    @property
    def data(self) -> RawBody:
        return self._raw_data


class JSONResponse(Response):
    @property
    def data(self) -> Dict:
        return json.loads(self._raw_data)
