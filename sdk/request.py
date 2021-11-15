import json
from typing import Optional
from urllib.parse import urlencode

import urllib3
from pydantic import HttpUrl, validate_arguments

from .decorators import chaining
from .enums import HTTPMethod
from .response import JSONResponse
from .typing import Body, Header, QueryParams


class Request:
    _safe_methods = [HTTPMethod.GET, HTTPMethod.HEAD]

    @validate_arguments
    def __init__(self, url: HttpUrl) -> None:
        self.url = url
        self._http = urllib3.PoolManager()
        self._method: Optional[HTTPMethod] = None
        self._body: Optional[Body] = None
        self._headers: Header = {}
        self._params: QueryParams = {}

    @property
    def method(self) -> Optional[HTTPMethod]:
        return self._method

    @method.setter
    def method(self, method: HTTPMethod) -> None:
        if self._method:
            raise ValueError(f"Method is already set to {self._method}")

        self._method = method

    @property
    def encoded_url(self):
        url = self.url

        if self._params:
            encoded_params = urlencode(self._params)
            url = f"{url}?{encoded_params}"

        return url

    @chaining
    def headers(self, **kwargs: Header) -> "Request":
        self._headers.update(**kwargs)

    @chaining
    def params(self, **kwargs: QueryParams) -> "Request":
        self._params.update(**kwargs)

    @chaining
    def get(self, **kwargs: QueryParams) -> "Request":
        self.method = HTTPMethod.GET
        self._params.update(**kwargs)

    @chaining
    def post(self, **kwargs: Body) -> "Request":
        self.method = HTTPMethod.POST
        self._body = kwargs

    @chaining
    def put(self, **kwargs: Body) -> "Request":
        self.method = HTTPMethod.PUT
        self._body = kwargs

    @chaining
    def patch(self, **kwargs: Body) -> "Request":
        self.method = HTTPMethod.PATCH
        self._body = kwargs

    @chaining
    def delete(self) -> "Request":
        self.method = HTTPMethod.DELETE

    @chaining
    def head(self) -> "Request":
        self.method = HTTPMethod.HEAD

    def json(self) -> JSONResponse:
        if not self._method:
            raise ValueError(
                "You need to set one HTTP method (get, post, put, patch, delete) beforehand"
            )

        self._headers.update({"Content-Type": "application/json"})

        http_response = self._json_request()
        json_response = self._process_json_response(http_response)
        return json_response

    def _json_request(self) -> urllib3.HTTPResponse:
        if self.method in self._safe_methods:
            http_response = self._http.request(
                self._method, self.encoded_url, headers=self._headers
            )

        else:
            data = json.dumps(self._body) if self._body else None
            http_response = self._http.request(
                self._method, self.encoded_url, body=data, headers=self._headers
            )

        return http_response

    def _process_json_response(
        self, http_response: urllib3.HTTPResponse
    ) -> JSONResponse:
        response = JSONResponse(
            data=http_response.data,
            status=http_response.status,
            headers=http_response.headers,
        )
        return response
