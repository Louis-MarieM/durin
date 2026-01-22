from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from ..value_objects.pipeline_state import PipelineState

@dataclass
class PipelineRun:
    pipeline_id: str
    state: PipelineState
    start: datetime
    end: datetime
    run_id: UUID = field(default_factory=uuid4)