from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict, Optional

from durin.domain import compute_natural_key, Currency, Interval, OHLCV, Source
from ..exceptions.application_exceptions import ApplicationValidationException

def _base_meta(ticker: str, period_start: datetime, loaded_at: datetime) -> dict:
    return {"ticker": ticker, "period_start": str(period_start), "loaded_at": str(loaded_at)}

@dataclass(frozen=True)
class OHLCVDTO():
    ticker: str
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    period_start: datetime
    interval: str
    source: str
    currency: str
    loaded_at: Optional[datetime] = field(default_factory=lambda: datetime.now(timezone.utc))
    volume: Optional[Decimal] = None
    adjusted_close_price: Optional[Decimal] = None
    meta: Optional[Dict[str, Any]] = None

    @property
    def natural_key(self):
        return compute_natural_key(self.ticker, self.interval, self.period_start)

    def __post_init__(self) -> None:
        self._validate_types()
        self._validate_timezones()

    def to_domain(self) -> OHLCV:
        return OHLCV(
            ticker=self.ticker,
            open_price=self.open_price,
            high_price=self.high_price,
            low_price=self.low_price,
            close_price=self.close_price,
            period_start=self.period_start,
            interval=Interval[self.interval],
            source=Source[self.source],
            currency=Currency[self.currency],
            loaded_at=self.loaded_at or datetime.now(timezone.utc),
            volume=self.volume,
            adjusted_close_price=self.adjusted_close_price
        )

    def _validate_types(self) -> None:
        base_meta = _base_meta(self.ticker, self.period_start, self.loaded_at)

        if not isinstance(self.ticker, str):
            raise ApplicationValidationException("ticker must be of type str.", meta={**base_meta, "ticker_type": type(self.ticker)})
        if not isinstance(self.open_price, Decimal):
            raise ApplicationValidationException("open_price must be of type Decimal.", meta={**base_meta, "open_price_type": type(self.open_price)})
        if not isinstance(self.high_price, Decimal):
            raise ApplicationValidationException("high_price must be of type Decimal.", meta={**base_meta, "high_price_type": type(self.high_price)})
        if not isinstance(self.low_price, Decimal):
            raise ApplicationValidationException("low_price must be of type Decimal.", meta={**base_meta, "low_price_type": type(self.low_price)})
        if not isinstance(self.close_price, Decimal):
            raise ApplicationValidationException("close_price must be of type Decimal.", meta={**base_meta, "close_price_type": type(self.close_price)})
        if not isinstance(self.period_start, datetime):
            raise ApplicationValidationException("period_start must be of type datetime.", meta={**base_meta, "period_start_type": type(self.period_start)})
        if not isinstance(self.interval, str):
            raise ApplicationValidationException("interval must be of type str.", meta={**base_meta, "interval_type": type(self.interval)})
        if not isinstance(self.source, str):
            raise ApplicationValidationException("source must be of type str.", meta={**base_meta, "source_type": type(self.source)})
        if not isinstance(self.currency, str):
            raise ApplicationValidationException("currency must be of type str.", meta={**base_meta, "currency_type": type(self.currency)})
        if self.loaded_at is not None and not isinstance(self.loaded_at, datetime):
            raise ApplicationValidationException("loaded_at must be of type datetime.", meta={**base_meta, "loaded_at_type": type(self.loaded_at)})
        if self.volume is not None and not isinstance(self.volume, Decimal):
            raise ApplicationValidationException("volume must be of type Decimal.", meta={**base_meta, "volume_type": type(self.volume)})
        if self.adjusted_close_price is not None and not isinstance(self.adjusted_close_price, Decimal):
            raise ApplicationValidationException("adjusted_close_price must be of type Decimal.", meta={**base_meta, "adjusted_close_price_type": type(self.adjusted_close_price)})

    def _validate_timezones(self) -> None:
        base_meta = _base_meta(self.ticker, self.period_start, self.loaded_at)
        
        if self.period_start.tzinfo is None:
            raise ApplicationValidationException("period_start must be timezone-aware.", meta=base_meta)
        if self.loaded_at.tzinfo is None:
            raise ApplicationValidationException("loaded_at must be timezone-aware.", meta=base_meta)