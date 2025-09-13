from dataclasses import dataclass
from typing import Any, Mapping, Optional, Protocol

@dataclass
class ProviderFactory(Protocol):

    def create(self, source: str, params: Optional[Mapping[str, Any]] = None) -> object:
        ...