from typing import Optional, Union

from .data import APIOptions
from .enums import HTTPMethod
from .request import Request
from .response import FormResponse, JSONResponse


class Endpoint:
    _meta: APIOptions
    collection_prefix: Optional[str]

    def __init__(
        self, name: Optional[str] = None, method: HTTPMethod = HTTPMethod.GET
    ) -> None:
        self.name = name
        self.method = method

    @property
    def url(self) -> str:
        base_url = self._meta.base_url.rstrip("/")
        collection_prefix = self.collection_prefix or ""
        endpoint = self.name.strip("/")

        composed_url = [base_url, collection_prefix, endpoint]
        return "/".join(composed_url)

    def __call__(self, *args, **kwargs) -> Union[JSONResponse, FormResponse]:
        request = Request(url=self.url)
        method = getattr(request, self.method, None)

        return method(*args, **kwargs)
