import pytest
from sdk import API, APIKeyAuthentication, Collection, Endpoint, HTTPMethod


def test_endpoint_should_initialize_without_collection_prefix():
    endpoint = Endpoint()

    assert endpoint.collection_prefix == ""


def test_endpoint_name_should_not_be_mandatory():
    endpoint = Endpoint()

    assert endpoint.name == None


def test_endpoint_should_fill_the_name_throught_the_api():
    class WeatherAPI(API):
        history = Endpoint()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    endpoint = api.history

    assert endpoint.name == "history"


def test_endpoint_api_should_keep_the_custom_endpoint_name():
    class WeatherAPI(API):
        history_by_city = Endpoint(name="history-by-city")

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    endpoint = api.history_by_city

    assert endpoint.name == "history-by-city"


def test_endpoint_should_compose_the_url():
    class WeatherAPI(API):
        info = Endpoint(name="", http_method=HTTPMethod.HEAD)
        history = Endpoint()
        history_by_city = Endpoint(name="history-by-city")

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()

    assert api.info.url == "https://weather.dev"
    assert api.history.url == "https://weather.dev/history"
    assert api.history_by_city.url == "https://weather.dev/history-by-city"


def test_endpoint_should_compose_the_url_within_a_collection():
    class ForecastCollection(Collection):
        temperature = Endpoint(name="")
        humidity = Endpoint(authenticated=True)
        by_city = Endpoint("by-city")

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()

    assert api.forecast.temperature.url == "https://weather.dev/forecast"
    assert api.forecast.humidity.url == "https://weather.dev/forecast/humidity"
    assert api.forecast.by_city.url == "https://weather.dev/forecast/by-city"


def test_endpoint_make_a_request():
    class WeatherAPI(API):
        history = Endpoint()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.history()

    assert request.url == "https://weather.dev/history"
    assert request.method == HTTPMethod.GET
    assert request._params == {}
    assert request._headers == {}


def test_endpoint_make_a_request_within_a_collection():
    class ForecastCollection(Collection):
        by_city = Endpoint("by-city")

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.forecast.by_city()

    assert request.url == "https://weather.dev/forecast/by-city"
    assert request.method == HTTPMethod.GET
    assert request._params == {}
    assert request._headers == {}


def test_endpoint_should_make_a_request_respecting_the_endpoint_method():
    class WeatherAPI(API):
        info = Endpoint(name="", http_method=HTTPMethod.HEAD)

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.info()

    assert request.method == HTTPMethod.HEAD


def test_endpoint_should_make_a_request_passing_the_kwargs():
    class WeatherAPI(API):
        history_by_city = Endpoint(name="history-by-city")

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.history_by_city(city="New York")

    assert request._params == {"city": "New York"}


def test_endpoint_should_accept_a_resource_identification():
    class ForecastCollection(Collection):
        by_zipcode = Endpoint(name=":zipcode")

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.forecast.by_zipcode(zipcode="5220125")

    assert request.url == "https://weather.dev/forecast/5220125"


def test_endpoint_should_accept_multiple_resource_identifiers():
    class ForecastCollection(Collection):
        by_city_and_region = Endpoint(name=":city/:region")

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()
    request = api.forecast.by_city_and_region(city="chicago", region="north")

    assert request.url == "https://weather.dev/forecast/chicago/north"


def test_endpoint_should_raise_an_exception_when_not_provide_the_required_uri():
    class ForecastCollection(Collection):
        by_zipcode = Endpoint(name=":zipcode")

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"

    api = WeatherAPI()

    with pytest.raises(ValueError) as exc:
        api.forecast.by_zipcode()

    assert str(exc.value) == "The URI zipcode was not defined."


def test_endpoint_should_authenticate_the_request_when_required():
    class ForecastCollection(Collection):
        humidity = Endpoint(authenticated=True)

    class WeatherAPI(API):
        forecast = ForecastCollection()

        class Meta:
            base_url = "https://weather.dev"
            authentication_class = APIKeyAuthentication

    api = WeatherAPI(api_key="bdd5f7bd-6afa-487d-ad7e-430ce6bd9796")
    request = api.forecast.humidity()

    assert request._headers == {"Authorization": "Bearer bdd5f7bd-6afa-487d-ad7e-430ce6bd9796"}
