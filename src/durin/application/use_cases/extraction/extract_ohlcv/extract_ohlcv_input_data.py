from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ....exceptions.application_exceptions import ApplicationException
from durin.domain import Interval, Source

def _base_meta(source: str, ticker: str, start: datetime, end: datetime, interval: str) -> dict:
    return {"source": source, "ticker": ticker, "start": str(start), "end": str(end), "interval": interval}

@dataclass(frozen=True)
class ExtractOHLCVInputData:
    source: str
    ticker: str
    start: datetime
    end: datetime
    interval: str

    def __post_init__(self):
        self._validate_types()
        self._validate_timezones()
        self._validate_business_rules()

    def _validate_types(self):
        base_meta = _base_meta(self.source, self.ticker, self.start, self.end, self.interval)

        if not Source.from_str_to_enum(self.source):
            raise ApplicationException(f"source input {self.source} not supported by Durin.")
        if not isinstance(self.ticker, str) or not self.ticker.strip():
            raise ApplicationException("ticker input must be a non-empty string.", meta=base_meta)
        if not isinstance(self.start, datetime) or not isinstance(self.end, datetime):
            raise ApplicationException("start and end inputs must be datetime instances.", meta=base_meta)
        if not Interval.from_str_to_enum(self.interval):
            raise ApplicationException(f"interval input {self.interval} not supported by Durin.")
    
    def _validate_timezones(self) -> None:
        base_meta = _base_meta(self.source, self.ticker, self.start, self.end, self.interval)
        
        if self.start.tzinfo is None:
            raise ApplicationException("start must be timezone-aware.", meta=base_meta)
        if self.end.tzinfo is None:
            raise ApplicationException("end must be timezone-aware.", meta=base_meta)

    def _validate_business_rules(self) -> None:
        base_meta = _base_meta(self.source, self.ticker, self.start, self.end, self.interval)

        if self.start >= self.end:
            raise ApplicationException("start input must be earlier than end input.", meta=base_meta)
        