from sdk import API, Collection, Endpoint


class CreditCardCollection(Collection):
    payment = Endpoint()


class PaymentAPI(API):
    credit_card = CreditCardCollection()

    class Meta:
        base_url = "https://payment.dev"


def test_collection_should_init_without_prefix_and_endpoints():
    collection = Collection()

    assert collection.collection_prefix == ""
    assert collection._endpoints == []


def test_collection_prefix_should_be_populated_throught_the_api():
    api = PaymentAPI()
    collection = api.credit_card

    assert collection.collection_prefix == "credit_card"


def test_collection_should_accept_endpoints():
    api = PaymentAPI()
    endpoint = api.credit_card.payment

    assert isinstance(endpoint, Endpoint)


def test_collection_should_set_the_endpoint_name():
    api = PaymentAPI()
    endpoint = api.credit_card.payment

    assert endpoint.name == "payment"
