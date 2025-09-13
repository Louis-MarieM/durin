from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from decimal import Decimal
import pytest

from durin.application import (
    OHLCVDTO,
    ApplicationValidationException,
)

from durin.domain import (
    OHLCV,
)

@pytest.fixture
def _valid_ohlcv_dto_fields() -> dict:
    start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    return dict(
        ticker="AAPL",
        open_price=Decimal("100"),
        high_price=Decimal("110"),
        low_price=Decimal("90"),
        close_price=Decimal("105"),
        period_start=start,
        interval="1d",
        source="Yahoo",
        currency="usd",
    )

def test_init__when_valid_fields__then_creates_OHLCVDTO_instance(_valid_ohlcv_dto_fields):
    obj = OHLCVDTO(**_valid_ohlcv_dto_fields)
    assert isinstance(obj, OHLCVDTO)

@pytest.mark.parametrize("field, bad_value", [
    ("ticker", 123),
    ("open_price", 100),
    ("high_price", 100),
    ("low_price", 100),
    ("close_price", 100),
    ("period_start", "01/01/2025"),
    ("interval", 100),
    ("source", 100),
    ("currency", 100),
    ("loaded_at", "2025/01/01"),
    ("volume", 100),
    ("adjusted_close_price", 100)
])
def test_init__when_type_invalid__then_raises_ApplicationValidationException(_valid_ohlcv_dto_fields, field, bad_value):
    args = _valid_ohlcv_dto_fields.copy()
    args[field] = bad_value
    with pytest.raises(ApplicationValidationException):
        OHLCVDTO(**args)

def test_init__when_timezone_not_valid__then_raises_ApplicationValidationException(_valid_ohlcv_dto_fields):
    args = _valid_ohlcv_dto_fields.copy()
    datetime_without_timezone = datetime(2025, 1, 1, 9, 30)
    args["period_start"] = datetime_without_timezone
    with pytest.raises(ApplicationValidationException):
        OHLCVDTO(**args)

def test_frozen__when_attempt_mutation__then_raises_FrozenInstanceError(_valid_ohlcv_dto_fields):
    obj = OHLCVDTO(**_valid_ohlcv_dto_fields)
    with pytest.raises(FrozenInstanceError):
        obj.ticker = "MSFT"
