from typing import List

from .endpoints import Endpoint


class CollectionMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._endpoints = []

        if not bases:
            return new_class

        for key, attr in attrs.items():
            if isinstance(attr, Endpoint):
                attr.name = key if attr.name is None else attr.name
                new_class._endpoints.append(attr)

            setattr(new_class, key, attr)

        return new_class


class Collection(metaclass=CollectionMeta):
    _endpoints: List[Endpoint]
    collection_prefix: str

    def __init__(self) -> None:
        self.collection_prefix = ""
