import json

from .typing import Header, RawBody


class Response:
    def __init__(self, data: RawBody, status: int, headers: Header) -> None:
        self._raw_data = data
        self._status = status
        self._headers = headers

    @property
    def raw_data(self) -> RawBody:
        return self._raw_data


class JSONResponse(Response):
    @property
    def data(self):
        return json.loads(self._raw_data)


class FormResponse(Response):
    @property
    def data(self):
        pass
