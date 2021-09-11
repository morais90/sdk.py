from abc import abstractclassmethod

from .request import Request


class Authentication:
    @abstractclassmethod
    def authenticate(self, **kwargs) -> Request:
        raise NotImplementedError


class APIKeyAuthentication(Authentication):
    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key

    def authenticate(self, url: str) -> Request:
        request = Request(url, default_params={"api_key": self.api_key})
        return request