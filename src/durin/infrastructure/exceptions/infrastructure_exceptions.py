from __future__ import annotations

from typing import Any, Optional
import json

from durin.application import ApplicationException

class InfrastructureException(ApplicationException):
    """Basic exception for all business errors."""
    def __init__(self, message: str, *, error_code: Optional[str] = None, meta: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or type(self).__name__
        self.meta = meta or {}

    def to_dict(self) -> dict[str, Any]:
        return {"error": self.error_code, "message": self.message, "meta": self.meta}
