from sdk import APIKeyAuthentication, Authentication, Request


def test_authentication_should_return_an_unchanged_request():
    request = Request(url="https://api.sdk.com")
    authentication = Authentication()
    authenticated_request = authentication.authenticate(request)

    assert authenticated_request._headers == {}
    assert authenticated_request._params == {}


def test_api_authentication_should_return_the_authorization_header():
    request = Request(url="https://api.sdk.com")
    authentication = APIKeyAuthentication(api_key="6d352e29-8d4c-4f61-b64e-b67b12c3808f")
    authenticated_request = authentication.authenticate(request)

    assert authenticated_request._headers == {"Authorization": "Bearer 6d352e29-8d4c-4f61-b64e-b67b12c3808f"}
