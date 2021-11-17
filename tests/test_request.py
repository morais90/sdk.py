from unittest.mock import patch

import pytest
from pydantic import ValidationError
from sdk import HTTPMethod, JSONResponse, Request


def test_request_init():
    url = "https://request.me"
    request = Request(url)

    assert request.url == url


def test_request_init_invalid_url():
    url = "websocket://request.me"

    with pytest.raises(ValidationError) as exc:
        Request(url)

    assert "URL scheme not permitted" in str(exc.value)


def test_request_should_set_the_GET_method():
    url = "https://request.me"
    request = Request(url).get()

    assert request.method == HTTPMethod.GET


def test_request_should_set_the_querystring_on_get():
    url = "https://request.me"
    request = Request(url).get(foo="bar", bar="foo")

    assert request._params == {"bar": "foo", "foo": "bar"}


def test_request_should_set_the_POST_method():
    url = "https://request.me"
    request = Request(url).post()

    assert request.method == HTTPMethod.POST


def test_request_should_set_the_request_body_on_post():
    url = "https://request.me"
    request = Request(url).post(price=11.20, discount=False)

    assert request._body == {
        "discount": False,
        "price": 11.2,
    }


def test_request_should_set_the_PUT_method():
    url = "https://request.me"
    request = Request(url).put()

    assert request.method == HTTPMethod.PUT


def test_request_should_set_the_request_body_on_put():
    url = "https://request.me"
    request = Request(url).put(due_at="2021-10-10", description="Just do it")

    assert request._body == {"description": "Just do it", "due_at": "2021-10-10"}


def test_request_should_set_the_PATCH_method():
    url = "https://request.me"
    request = Request(url).patch()

    assert request.method == HTTPMethod.PATCH


def test_request_should_set_the_request_body_on_patch():
    url = "https://request.me"
    request = Request(url).patch(apply_immediately=False, email="an@email.com")

    assert request._body == {"apply_immediately": False, "email": "an@email.com"}


def test_request_should_accept_new_params():
    url = "https://request.me"
    request = Request(url).get(foo="bar", bar="foo").params(baz="baz")

    assert request._params == {
        "bar": "foo",
        "baz": "baz",
        "foo": "bar",
    }


def test_request_should_accept_headers():
    url = "https://request.me"
    request = Request(url).post(turn_off=True).headers(**{"X-Server": "X08376"})

    assert request._headers == {"X-Server": "X08376"}


def test_request_should_handle_readonly_methods_on_json_request():
    url = "https://request.me"
    request = Request(url).get(foo="bar")

    with patch.object(request, "_http") as pool:
        request.json()

        pool.request.assert_called_with(
            HTTPMethod.GET,
            "https://request.me?foo=bar",
            headers={"Content-Type": "application/json"},
        )


def test_request_should_handle_writeonly_methods_on_json_request():
    url = "https://request.me"
    request = Request(url).post(foo="bar")

    with patch.object(request, "_http") as pool:
        request.json()

        pool.request.assert_called_with(
            HTTPMethod.POST,
            "https://request.me",
            body='{"foo": "bar"}',
            headers={"Content-Type": "application/json"},
        )


def test_request_should_return_a_json_response_on_json_request():
    url = "https://request.me"
    request = Request(url).get(foo="bar")

    with patch.object(request, "_http"):
        response = request.json()

        assert isinstance(response, JSONResponse)


def test_request_should_check_for_the_method_on_return_the_json_request():
    url = "https://request.me"
    request = Request(url)

    with pytest.raises(ValueError) as exc:
        request.json()

    assert "You need to set one HTTP method (get, post, put, patch, delete) beforehand" in str(exc.value)
