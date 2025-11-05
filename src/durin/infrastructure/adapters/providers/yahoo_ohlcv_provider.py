from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Iterable, Mapping, Optional

try:
    import pandas as pd
    import yfinance as yf
except:
    pd = None
    yf = None

from ...exceptions.infrastructure_exceptions import InfrastructureException
from durin.config.logger import logger
from durin.domain import Currency, Interval, OHLCV, Source
from durin.application import ApplicationException

def _validate_inputs(ticker: str, start: datetime, end: datetime, interval: str) -> None:
    if not isinstance(ticker, str) or not ticker.strip():
        raise InfrastructureException("ticker input must be a non-empty string.", meta={"ticker": ticker})
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise InfrastructureException("start and end inputs must be datetime instances.", meta={"ticker": ticker, "start": start, "end": end})
    if start.tzinfo is None or end.tzinfo is None:
        raise InfrastructureException("start and end inputs must be timezone-aware datetimes.", meta={"ticker": ticker, "start": start, "end": end})
    if start >= end:
        raise InfrastructureException("start input must be earlier than end input.", meta={"ticker": ticker, "start": start, "end": end})
    if not Interval.from_str_to_enum(interval):
        raise InfrastructureException(f"interval input {interval} not supported by YFinance.")

def _to_decimal(value: Any) -> Decimal:
    if pd.isna(value):
        raise InfrastructureException("Value is NaN.")
    if value is None:
        raise InfrastructureException("Value is None.")
    if isinstance(value, Decimal):
        return value
    
    try:
        return Decimal(str(value))
    except Exception as exception:
        raise InfrastructureException(f"Cannot convert {value} to Decimal", meta={"exception": exception})

class YahooOHLCVProvider:

    def __init__(self, client: Optional[Any] = None, timeout: int = 30):
        # Provider allows client injection/mocking (default: yfinance)
        self.client = client or yf
        self.timeout = timeout

    def fetch(self, ticker: str, start: datetime, end: datetime, interval: str, params: Optional[Mapping[str, Any]] = None) -> Iterable[OHLCV]:
        try:
            _validate_inputs(ticker, start, end, interval)
            for raw_row in self._call_yfinance(ticker, start, end, interval, adjust_price=False):
                try:
                    ohlcv = self._from_raw_to_entities(raw_row, ticker, interval)
                    yield ohlcv
                except Exception as exception:
                    logger.warning("Failed to convert raw Yahoo row to OHLCV", exc_info=exception, extra={"ticker": ticker})
                    continue
            return
        except InfrastructureException as infrastructure_exception:
            raise InfrastructureException("Yahoo finance service is unreachable or in error.", meta={"ticker": ticker, "start": start, "end": end, "interval": interval, "exception": infrastructure_exception})
        except Exception as exception:
            raise InfrastructureException("Unknown error.", meta={"ticker": ticker, "start": start, "end": end, "interval": interval, "exception": exception})

    def _call_yfinance(self, ticker: str, start: datetime, end: datetime, interval: str, adjust_price: bool) -> Iterable[OHLCV]:
        try:
            ticker_yf = self.client.Ticker(ticker)
            ticker_history_dataframe = ticker_yf.history(start=start, end=end, interval=interval, auto_adjust=adjust_price)
        except Exception as exception:
            raise ApplicationException("Yahoo finance service is unreachable or in error.", meta={"ticker": ticker, "start": start, "end": end, "interval": interval, "exception": exception})
        
        if ticker_history_dataframe.empty:
            return
        
        if ticker_history_dataframe.index.tz is None:
            ticker_history_dataframe.index = ticker_history_dataframe.index.tz_localize(timezone.utc)
        else:
            ticker_history_dataframe.index = ticker_history_dataframe.index.tz_convert(timezone.utc)
        
        # itertuples: fast and returns a namedtuple, first field is Index by default.
        for row in ticker_history_dataframe.itertuples(index=True, name="Row"):
            # row.Index, row.Open, row.High...
            yield row

    def _from_raw_to_entities(self, raw_row: dict, ticker: str, interval: str)-> OHLCV:
        raw_open_price = getattr(raw_row, "Open", None)
        raw_high_price = getattr(raw_row, "High", None)
        raw_low_price = getattr(raw_row, "Low", None)
        raw_close_price = getattr(raw_row, "Close", None)
        raw_period_start = getattr(raw_row, "Index", None)
        raw_volume = getattr(raw_row, "Volume", None)
        raw_adjusted_close_price = getattr(raw_row, "Adj Close", None)

        open_price = _to_decimal(raw_open_price)
        high_price = _to_decimal(raw_high_price)
        low_price = _to_decimal(raw_low_price)
        close_price = _to_decimal(raw_close_price)
        volume = _to_decimal(raw_volume)
        adjusted_close_price = None
        if not raw_adjusted_close_price is None:
            adjusted_close_price = _to_decimal(raw_adjusted_close_price)
        
        if raw_period_start.tzinfo is None:
            period_start = raw_period_start.replace(tzinfo=timezone.utc)
        else:
            period_start = raw_period_start.astimezone(timezone.utc)
        period_start = period_start.replace(microsecond=0)

        loaded_at = datetime.now(timezone.utc)

        return OHLCV(
            ticker=ticker,
            open_price=open_price,
            high_price=high_price,
            low_price=low_price,
            close_price=close_price,
            period_start=period_start,
            interval=Interval(interval),
            source=Source.YAHOO,
            currency=Currency.USD,
            loaded_at=loaded_at,
            volume=volume,
            adjusted_close_price=adjusted_close_price
        )
