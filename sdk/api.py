import dataclasses
from typing import List

from .collections import Collection
from .data import APIOptions
from .endpoints import Endpoint


class APIMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)

        if not bases:
            return new_class

        new_class._collections = []
        new_class._endpoints = []
        meta = getattr(new_class, "Meta", None)

        if not meta:
            raise AttributeError(
                f"Meta configuration was not declared at the class {new_class.__name__}"
            )

        options = {}
        missing_fields = []

        for field in dataclasses.fields(APIOptions):
            value = getattr(meta, field.name, None)
            has_default_value = (
                field.default != dataclasses.MISSING
                or field.default_factory != dataclasses.MISSING
            )

            if not value and not has_default_value:
                missing_fields.append(field.name)

            if value:
                options[field.name] = value

        if missing_fields:
            formatted_missing_fields = ", ".join(missing_fields)
            raise AttributeError(
                f"The follow fields were not declared at the Meta: {formatted_missing_fields}"
            )

        new_class._meta = APIOptions(**options)

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

    def __init__(self, **kwargs) -> None:
        endpoints = [endpoint for c in self._collections for endpoint in c._endpoints]
        endpoints.extend(self._endpoints)

        self._meta.kwargs.update(**kwargs)

        for endpoint in endpoints:
            endpoint._meta = self._meta
