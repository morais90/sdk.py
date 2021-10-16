from dataclasses import dataclass, field
from typing import Any, Dict

from .authentication import APIKeyAuthentication, Authentication


@dataclass(frozen=True)
class APIOptions:
    base_url: str
    authentication_class: Authentication = APIKeyAuthentication
    kwargs: Dict[str, Any] = field(default_factory=dict)
