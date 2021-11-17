from sdk import JSONResponse, Response


def test_response_init():
    response = Response(data=b"just a response", status=200, headers={"cache-control": "no-cache"})

    assert response.status == 200
    assert response.headers == {"cache-control": "no-cache"}
    assert response.raw_data == b"just a response"
    assert response.data == b"just a response"


def test_json_response_should_loads_the_content():
    response = JSONResponse(data=b'{"foo": "bar"}', status=200, headers={"cache-control": "no-cache"})

    assert response.status == 200
    assert response.headers == {"cache-control": "no-cache"}
    assert response.raw_data == b'{"foo": "bar"}'
    assert response.data == {"foo": "bar"}
