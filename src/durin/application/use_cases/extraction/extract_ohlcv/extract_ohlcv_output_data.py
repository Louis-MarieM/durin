from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from durin.domain import OHLCV

@dataclass(frozen=True)
class ExtractOHLCVOutputData:
    ohlcv_list: Iterable[OHLCV]