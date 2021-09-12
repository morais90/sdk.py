import pytest
from sdk import API, Collection, Endpoint, APIKeyAuthentication


class VoidAPI(API):
    class Meta:
        base_url = "http://void.api/"


class UserAPI(API):
    list = Endpoint()
    get = Endpoint()

    class Meta:
        base_url = "http://user.api/"


class ImageCollection(Collection):
    info = Endpoint()
    vote = Endpoint()


class VideoCollection(Collection):
    watch = Endpoint()
    mark_as_viewed = Endpoint()


class FileAPI(API):
    images = ImageCollection()
    videos = VideoCollection()

    class Meta:
        base_url = "http://file.api/"


def test_api_should_initialize_the_meta_configuration():
    api = VoidAPI()

    assert api._meta.base_url == "http://void.api/"
    assert api._meta.authentication_class == APIKeyAuthentication


def test_api_should_require_the_meta_configuration():
    with pytest.raises(AttributeError) as exc:

        class APIWithoutMeta(API):
            pass

    expected = "Meta configuration was not declared at the class APIWithoutMeta"
    assert str(exc.value) == expected


def test_api_should_verify_the_required_fields():
    with pytest.raises(AttributeError) as exc:

        class APIWithoutRequiredFields(API):
            class Meta:
                pass

    assert str(exc.value) == "The follow fields were not declared at the Meta: base_url"


def test_api_should_accept_endpoints():
    api = UserAPI()

    assert isinstance(api.list, Endpoint)
    assert isinstance(api.get, Endpoint)


def test_api_should_transpose_the_meta_to_the_endpoints():
    api = UserAPI()

    assert api.list._meta == api._meta
    assert api.get._meta == api._meta


def test_api_should_set_the_name_of_the_endpoints():
    api = UserAPI()

    assert api.list.name == "list"
    assert api.get.name == "get"


def test_api_should_accept_collections():
    api = FileAPI()

    assert isinstance(api.images, Collection)
    assert isinstance(api.videos, Collection)


def test_api_should_set_the_prefix_of_the_collections():
    api = FileAPI()

    assert api.images.collection_prefix == "images"
    assert api.videos.collection_prefix == "videos"


def test_api_should_transpose_the_meta_to_the_collections_endpoints():
    api = FileAPI()

    assert api.images.info._meta == api._meta
    assert api.images.vote._meta == api._meta
    assert api.videos.watch._meta == api._meta
    assert api.videos.mark_as_viewed._meta == api._meta


def test_api_should_not_overwrite_the_endpoints_alias_name():
    class AliasAPI(API):
        detail = Endpoint(name="")
        nickname = Endpoint(name="my-nickname")

        class Meta:
            base_url = "https://alias.api"

    api = AliasAPI()

    assert api.detail.name == ""
    assert api.nickname.name == "my-nickname"