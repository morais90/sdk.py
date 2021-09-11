from typing import List

from .collection import Collection
from .data import APIOptions
from .endpoint import Endpoint


class APIMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        if not bases:
            return new_class

        new_class._collections = []
        new_class._endpoints = []
        meta = getattr(new_class, "Meta", None)

        if meta:
            authentication_class = getattr(meta, "authentication_class")
            new_class._meta = APIOptions(
                base_url=meta.base_url, authentication_class=authentication_class
            )

        for key, attr in attrs.items():
            if isinstance(attr, Collection):
                attr.collection_prefix = key
                attr._meta = new_class._meta
                new_class._collections.append(attr)

                for endpoint in attr._endpoints:
                    endpoint.collection_prefix = key

            if isinstance(attr, Endpoint):
                attr.name = key if attr.name is None else attr.name
                attr._meta = new_class._meta
                new_class._endpoints.append(attr)

            setattr(new_class, key, attr)

        return new_class


class API(metaclass=APIMeta):
    _meta: APIOptions
    _collections: List[Collection]
    _endpoints: List[Endpoint]

    def __init__(self) -> None:
        endpoints = [endpoint for c in self._collections for endpoint in c._endpoints]
        endpoints.extend(self._endpoints)

        for endpoint in endpoints:
            endpoint._meta = self._meta
