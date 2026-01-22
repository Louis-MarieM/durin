from __future__ import annotations

from typing import Any, Optional

class DomainException(Exception):
    """Basic exception for all business errors."""
    def __init__(self, message: str, *, error_code: Optional[str] = None, meta: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or type(self).__name__
        self.meta = meta or {}

    def to_dict(self) -> dict[str, Any]:
        return {"error": self.error_code, "message": self.message, "meta": self.meta}

class ValidationException(DomainException):
    """Structural or format validation."""

class InvalidOHLCVException(ValidationException):
    """OHLCV invariants violated (inconsistent high/low/open/close)."""

class InvalidPipelineException(ValidationException):
    """Pipeline definition or step invariants violated (presence of cycle, inconsistent step runner...)."""

class PipelineOperationNotPermitted(DomainException):
    """Actual pipeline state don't permit the operation."""

class DataConflictException(DomainException):
    """Conflict (duplicate/unique key)."""

class RepositoryException(DomainException):
    """Access/persistence error (repository abstraction)."""