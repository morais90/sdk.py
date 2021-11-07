from .request import Request


class Authentication:
    def authenticate(self, request: Request) -> Request:
        return request


class APIKeyAuthentication(Authentication):
    _keyword: str = "Bearer"

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self._api_key = api_key

    def authenticate(self, request: Request) -> Request:
        api_key = f"{self._keyword} {self._api_key}"

        return request.headers(**{"Authorization": api_key})