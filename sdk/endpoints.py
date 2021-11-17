import re
from typing import Any, Dict, Optional

from .authentications import Authentication
from .data import APIOptions
from .enums import HTTPMethod
from .request import Request
from .response import JSONResponse

URI_PATTERN = re.compile(r":(\w+)")


class Endpoint:
    _meta: APIOptions
    collection_prefix: str

    def __init__(
        self,
        name: Optional[str] = None,
        http_method: HTTPMethod = HTTPMethod.GET,
        authenticated: bool = False,
    ) -> None:
        self.collection_prefix = ""
        self.name = name
        self.http_method = http_method
        self.authenticated = authenticated
        self._uri: Dict[str, str] = {}

    @property
    def url(self) -> str:
        base_url = self._meta.base_url.rstrip("/")
        collection_prefix = self.collection_prefix
        endpoint = self.name.strip("/")

        for uri, value in self._uri.items():
            endpoint = endpoint.replace(f":{uri}", value)

        composed_url = (base_url, collection_prefix, endpoint)
        composed_url = (path for path in composed_url if path)
        return "/".join(composed_url)

    def __call__(self, **kwargs) -> JSONResponse:
        request_args = self._before_request(**kwargs)

        request = self._create_request()
        http_method = self.http_method.value.lower()
        method = getattr(request, http_method, None)

        return method(**request_args)

    def _before_request(self, **kwargs) -> Dict[str, Any]:
        request_args = self._check_for_resource_identifier(**kwargs)

        return request_args

    def _check_for_resource_identifier(self, **kwargs) -> Dict[str, Any]:
        uris = URI_PATTERN.findall(self.name)
        self._uri = {}

        for uri in uris:
            value = kwargs.pop(uri, None)

            if not value:
                raise ValueError(f"The URI {uri} was not defined.")

            self._uri[uri] = str(value)

        return kwargs

    def _create_request(self) -> Request:
        request = Request(url=self.url)

        if self.authenticated:
            authentication = self.get_authentication()
            request = authentication.authenticate(request)

        return request

    def get_authentication(self) -> Authentication:
        kwargs = self._meta.kwargs
        return self._meta.authentication_class(**kwargs)
