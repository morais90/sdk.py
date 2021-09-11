from abc import abstractclassmethod

from .request import Request


class Authentication:
    @abstractclassmethod
    def authenticate(self, url: str) -> Request:
        raise NotImplementedError


class APIKeyAuthentication(Authentication):
    def __init__(
        self,
        api_key: str,
        keyword: str = "Bearer",
    ) -> None:
        super().__init__()
        self._api_key = api_key
        self._keyword = keyword

    def authenticate(self, url: str) -> Request:
        api_key = f"{self._keyword} {self._api_key}"
        request = Request(url).headers({"Authorization": api_key})

        return request