from datetime import datetime, timezone

from ..exceptions.domain_exceptions import DomainException

def compute_natural_key(ticker: str, interval: str, period_start: datetime) -> str:
    try:
        _validate_fields(ticker, interval, period_start)
        ticker_standardized = ticker.strip().upper()
        interval_standardized = interval.strip().lower()
        period_start_standardized = _standardize_datetime(period_start)
        return f"{ticker_standardized}|{interval_standardized}|{period_start_standardized}"
    except DomainException:
        raise DomainException("Fields must be not None.", meta={"ticker": ticker, "interval": interval, "period_start": datetime})
    except:
        raise DomainException("An unknown error has occured.", meta={"ticker": ticker, "interval": interval, "period_start": datetime})

def _validate_fields(ticker: str, interval: str, period_start: datetime) -> None:
    if ticker is None:
        raise DomainException("ticker must not be None.", meta={"ticker": ticker})
    if interval is None:
        raise DomainException("interval must not be None.", meta={"interval": interval})
    if period_start is None:
        raise DomainException("period_start must not be None.", meta={"period_start": period_start})

def _standardize_datetime(date: datetime) -> str:
    """Ensure timezone-aware UTC and remove microseconds, format with 'Z'."""
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    else:
        date = date.astimezone(timezone.utc)
    date = date.replace(microsecond=0)
    return date.isoformat().replace('+00:00', 'Z')
