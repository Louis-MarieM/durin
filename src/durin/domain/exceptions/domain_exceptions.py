from __future__ import annotations

from typing import Any, Dict, Optional

class DomainException(Exception):
    """Basic exception for all business errors."""
    def __init__(self, message: str, *, error_code: Optional[str] = None, meta: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or type(self).__name__
        self.meta = meta or {}

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.error_code, "message": self.message, "meta": self.meta}

class ValidationException(DomainException):
    """Structural or format validation."""

class InvalidOHLCVException(ValidationException):
    """OHLCV invariants violated (inconsistent high/low/open/close)."""

class DataConflictException(DomainException):
    """Conflict (duplicate/unique key)."""

class RepositoryException(DomainException):
    """Access/persistence error (repository abstraction)."""