from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from ..value_objects.step_state import StepState

@dataclass
class StepRun:
    step_id: str
    pipeline_run_id: UUID
    state: StepState
    start: datetime
    end: datetime
    try_number: int
    run_id: UUID = field(default_factory=uuid4)