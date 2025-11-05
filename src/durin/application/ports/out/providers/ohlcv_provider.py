from datetime import datetime
from typing import Any, Iterable, Mapping, Optional, Protocol

from durin.domain import Interval, OHLCV

class OHLCVProvider(Protocol):

    def fetch(self, ticker: str, start: datetime, end: datetime, interval: Interval, params: Optional[Mapping[str, Any]] = None) -> Iterable[OHLCV]:
        ...