from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ExtractOHLCVInputData:
    source: str
    ticker: str
    start: datetime
    end: datetime
    interval: str