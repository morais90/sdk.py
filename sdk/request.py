import json
from typing import Optional
from urllib.parse import urlencode

import pydantic
import urllib3

from .decorators import chaining
from .enums import HTTPMethod
from .response import FormResponse, JSONResponse
from .typing import Body, Header, QueryParams


class Request:
    _safe_methods = [HTTPMethod.GET, HTTPMethod.HEAD]

    def __init__(self, url: pydantic.HttpUrl = None) -> None:
        self._http = urllib3.PoolManager()
        self.url = url
        self._method: Optional[HTTPMethod] = None
        self._headers: Header = {}
        self._params: QueryParams = {}
        self._body: Body = {}

    @property
    def method(self) -> Optional[HTTPMethod]:
        return self._method

    @method.setter
    def set_method(self, method: HTTPMethod) -> None:
        if self._method:
            raise ValueError("Method is already set to {self._method}")

        self._method = method

    @property
    def encoded_url(self):
        url = self.url

        if self._params:
            encoded_params = urlencode(self._params)
            url = f"{url}?{encoded_params}"

        return url

    @chaining
    def headers(self, headers: Header) -> "Request":
        self._headers.update(**headers)

    @chaining
    def params(self, params: QueryParams) -> "Request":
        self._params.update(**params)

    @chaining
    def get(self, params: QueryParams = None) -> "Request":
        self.method = HTTPMethod.GET
        self._params.update(**params)

    @chaining
    def post(self, data: Body = None) -> "Request":
        self.method = HTTPMethod.POST
        self._body = data

    @chaining
    def put(self, data: Body = None) -> "Request":
        self.method = HTTPMethod.PUT
        self._body = data

    @chaining
    def patch(self, data: Body = None) -> "Request":
        self.method = HTTPMethod.PATCH
        self._body = data

    @chaining
    def delete(self) -> "Request":
        self.method = HTTPMethod.DELETE

    def json(self) -> JSONResponse:
        if not self._method:
            raise ValueError(
                "You need to call one method (get, post, put, patch, delete)"
            )

        self._headers.update({"Content-Type": "application/json"})

        http_response = self._json_request()
        json_response = self._process_json_response(http_response)
        return json_response

    def form(self) -> FormResponse:
        if not self._method:
            raise ValueError("You need to call one method (post, put, patch)")

        if self.method in self._safe_methods:
            raise ValueError(f"Method {self.method} is not supported in form")

        http_response = self._form_request()
        response = self._process_form_response(http_response)
        return response

    def _json_request(self) -> urllib3.HTTPResponse:
        if self.method in self._safe_methods:
            http_response = self._http.request(
                self._method, self.encoded_url, headers=self._headers
            )

        else:
            data = json.loads(self._body) if self._body else None
            http_response = self._http.request(
                self._method, self.encoded_url, body=data, headers=self._headers
            )

        return http_response

    def _form_request(self) -> urllib3.HTTPResponse:
        http_response = self._http.request(
            self._method, self.encoded_url, fields=self._body, headers=self._headers
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

    def _proces_form_response(
        self, http_response: urllib3.HTTPResponse
    ) -> FormResponse:
        response = FormResponse(
            data=http_response.data,
            status=http_response.status,
            headers=http_response.headers,
        )
        return response
