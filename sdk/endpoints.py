from typing import Optional, Union

from .authentications import Authentication
from .data import APIOptions
from .enums import HTTPMethod
from .request import Request
from .response import FormResponse, JSONResponse


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

    @property
    def url(self) -> str:
        base_url = self._meta.base_url.rstrip("/")
        collection_prefix = self.collection_prefix
        endpoint = self.name.strip("/")

        composed_url = (base_url, collection_prefix, endpoint)
        composed_url = (path for path in composed_url if path)
        return "/".join(composed_url)

    def get_authentication(self) -> Authentication:
        kwargs = self._meta.kwargs
        return self._meta.authentication_class(**kwargs)

    def _create_request(self) -> Request:
        request = Request(url=self.url)

        if self.authenticated:
            authentication = self.get_authentication()
            request = authentication.authenticate(request)

        return request

    def __call__(self, **kwargs) -> Union[JSONResponse, FormResponse]:
        request = self._create_request()
        http_method = self.http_method.value.lower()
        method = getattr(request, http_method, None)

        return method(**kwargs)
