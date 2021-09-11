from dataclasses import dataclass
from .authentication import Authentication, APIKeyAuthentication


@dataclass
class APIOptions:
    base_url: str
    authentication_class: Authentication = APIKeyAuthentication
