from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from ..exceptions.domain_exceptions import ValidationException, InvalidOHLCVException
from ..value_objects.currency import Currency
from ..value_objects.interval import Interval
from ..value_objects.source import Source

def _base_meta(ticker: str, period_start: datetime, loaded_at: datetime) -> dict:
    return {"ticker": ticker, "period_start": str(period_start), "loaded_at": str(loaded_at)}

@dataclass(frozen=True)
class OHLCV:
    ticker: str
    open_price: Decimal
    high_price: Decimal
    low_price: Decimal
    close_price: Decimal
    period_start: datetime
    interval: Interval
    source: Source
    currency: Currency
    loaded_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    volume: Optional[Decimal] = None
    adjusted_close_price: Optional[Decimal] = None

    def __post_init__(self):
        self._validate_types()
        self._validate_timezones()
        self._validate_bounds_and_relations()
    
    def __eq__(self, other: object) -> bool:
        """Equality key = (ticker, period_start, interval)"""
        if not isinstance(other, OHLCV):
            return NotImplemented
        return (
            self.ticker == other.ticker
            and self.period_start == other.period_start
            and self.interval == other.interval
            )

    def __lt__(self, other: object) -> bool:
        """It only for same ticker. Order by period_start."""
        if not isinstance(other, OHLCV):
            return NotImplemented
        if self.ticker != other.ticker:
            return NotImplemented
        return self.period_start < other.period_start

    def _validate_types(self) -> None:
        base_meta = _base_meta(self.ticker, self.period_start, self.loaded_at)

        if not isinstance(self.ticker, str):
            raise ValidationException("ticker must be of type str.", meta={**base_meta, "ticker_type": type(self.ticker)})
        if not isinstance(self.open_price, Decimal):
            raise ValidationException("open_price must be of type Decimal.", meta={**base_meta, "open_price_type": type(self.open_price)})
        if not isinstance(self.high_price, Decimal):
            raise ValidationException("high_price must be of type Decimal.", meta={**base_meta, "high_price_type": type(self.high_price)})
        if not isinstance(self.low_price, Decimal):
            raise ValidationException("low_price must be of type Decimal.", meta={**base_meta, "low_price_type": type(self.low_price)})
        if not isinstance(self.close_price, Decimal):
            raise ValidationException("close_price must be of type Decimal.", meta={**base_meta, "close_price_type": type(self.close_price)})
        if not isinstance(self.period_start, datetime):
            raise ValidationException("period_start must be of type datetime.", meta={**base_meta, "period_start_type": type(self.period_start)})
        if not isinstance(self.interval, Interval):
            raise ValidationException("interval must be of type Interval.", meta={**base_meta, "interval_type": type(self.interval)})
        if not isinstance(self.source, Source):
            raise ValidationException("source must be of type Source.", meta={**base_meta, "source_type": type(self.source)})
        if not isinstance(self.currency, Currency):
            raise ValidationException("currency must be of type Currency.", meta={**base_meta, "currency_type": type(self.currency)})
        if not isinstance(self.loaded_at, datetime):
            raise ValidationException("loaded_at must be of type datetime.", meta={**base_meta, "loaded_at_type": type(self.loaded_at)})
        if self.volume is not None and not isinstance(self.volume, Decimal):
            raise ValidationException("volume must be of type Decimal.", meta={**base_meta, "volume_type": type(self.volume)})
        if self.adjusted_close_price is not None and not isinstance(self.adjusted_close_price, Decimal):
            raise ValidationException("adjusted_close_price must be of type Decimal.", meta={**base_meta, "adjusted_close_price_type": type(self.adjusted_close_price)})

    def _validate_timezones(self) -> None:
        base_meta = _base_meta(self.ticker, self.period_start, self.loaded_at)
        
        if self.period_start.tzinfo is None:
            raise ValidationException("period_start must be timezone-aware.", meta=base_meta)
        if self.loaded_at.tzinfo is None:
            raise ValidationException("loaded_at must be timezone-aware.", meta=base_meta)

    def _validate_bounds_and_relations(self) -> None:
        base_meta = _base_meta(self.ticker, self.period_start, self.loaded_at)

        max_price = max(self.open_price, self.low_price, self.close_price)
        min_price = min(self.open_price, self.high_price, self.close_price)

        if self.high_price < max_price:
            raise InvalidOHLCVException("high_price inconsistent with open/low/close.", meta={**base_meta, "high_price": str(self.high_price), "max_price": str(max_price)})
        if self.low_price > min_price:
            raise InvalidOHLCVException("low_price inconsistent with open/high/close.", meta={**base_meta, "low_price": str(self.low_price), "min_price": str(min_price)})
        if self.volume is not None and self.volume < Decimal("0"):
            raise InvalidOHLCVException("volume cannot be negative.", meta={**base_meta, "volume": str(self.volume)})
        if self.loaded_at < self.period_start:
            raise InvalidOHLCVException("loaded_at is earlier than period_start.", meta=base_meta)
