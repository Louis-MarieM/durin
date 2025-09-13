from datetime import datetime
from typing import Any, Iterable, Mapping, Optional, Protocol

from ...schemas.ohlcv_dto import OHLCVDTO

class OHLCVProvider(Protocol):

    def fetch(self, ticker: str, start: datetime, end: datetime, interval: str, params: Optional[Mapping[str, Any]] = None) -> Iterable[OHLCVDTO]:
        ...