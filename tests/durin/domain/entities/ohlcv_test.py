from dataclasses import FrozenInstanceError
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pytest

from durin.domain import (
    Currency, 
    Interval, 
    InvalidOHLCVException, 
    OHLCV, 
    Source, 
    ValidationException,
)

@pytest.fixture
def _valid_ohlcv_fields() -> dict:
    start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    return dict(
        ticker="AAPL",
        open_price=Decimal("100"),
        high_price=Decimal("110"),
        low_price=Decimal("90"),
        close_price=Decimal("105"),
        period_start=start,
        interval=Interval.ONE_DAY,
        source=Source.YAHOO,
        currency=Currency.USD,
        loaded_at=start + timedelta(seconds=1),
    )

def test_init__when_valid_fields__then_creates_OHLCV_instance(_valid_ohlcv_fields):
    obj = OHLCV(**_valid_ohlcv_fields)
    assert isinstance(obj, OHLCV)

@pytest.mark.parametrize("field, bad_value", [
    ("ticker", 123),
    ("open_price", 100),
    ("high_price", 100),
    ("low_price", 100),
    ("close_price", 100),
    ("period_start", "01/01/2025"),
    ("interval", "1d"),
    ("source", "YAHOO"),
    ("currency", "USD"),
    ("loaded_at", "2025/01/01"),
    ("volume", 100),
    ("adjusted_close_price", 100)
])
def test_init__when_type_invalid__then_raises_ValidationException(_valid_ohlcv_fields, field, bad_value):
    args = _valid_ohlcv_fields.copy()
    args[field] = bad_value
    with pytest.raises(ValidationException):
        OHLCV(**args)

def test_init__when_timezone_not_valid__then_raises_ValidationException(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    datetime_without_timezone = datetime(2025, 1, 1, 9, 30)
    args["period_start"] = datetime_without_timezone
    with pytest.raises(ValidationException):
        OHLCV(**args)

def test_init__when_high_price_not_max__then_raises_InvalidOHLCVException(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    args["close_price"] = Decimal("1000")
    with pytest.raises(InvalidOHLCVException):
        OHLCV(**args)

def test_init__when_low_price_not_min__then_raises_InvalidOHLCVException(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    args["close_price"] = Decimal("10")
    with pytest.raises(InvalidOHLCVException):
        OHLCV(**args)

def test_init__when_volume_zero__then_creates_OHLCV_instance(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    args["volume"] = Decimal("0")
    obj = OHLCV(**args)
    assert isinstance(obj, OHLCV)

def test_init__when_volume_negative__then_raises_InvalidOHLCVException(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    args["volume"] = Decimal("-10")
    with pytest.raises(InvalidOHLCVException):
        OHLCV(**args)

def test_init__when_dates_inconsistent__then_raises_InvalidOHLCVException(_valid_ohlcv_fields):
    args = _valid_ohlcv_fields.copy()
    date = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    args["period_start"] = date + timedelta(seconds=1)
    args["loaded_at"] = date - timedelta(seconds=1)
    with pytest.raises(InvalidOHLCVException):
        OHLCV(**args)

def test_eq__when_same_key_fields__then_returns_true(_valid_ohlcv_fields):
    obj_1 = OHLCV(**_valid_ohlcv_fields)
    obj_2 = OHLCV(**_valid_ohlcv_fields)
    assert obj_1 == obj_2

def test_eq__when_different_key_field__then_returns_false(_valid_ohlcv_fields):
    obj_1 = OHLCV(**_valid_ohlcv_fields)
    args = _valid_ohlcv_fields.copy()
    args["ticker"] = "MSFT"
    obj_2 = OHLCV(**args)
    assert not obj_1 == obj_2

def test_eq__when_different_types__then_returns_false(_valid_ohlcv_fields):
    obj_1 = OHLCV(**_valid_ohlcv_fields)
    args = _valid_ohlcv_fields.copy()
    assert not obj_1 == args

def test_lt__when_objects_comparable__then_orders(_valid_ohlcv_fields):
    args_01 = _valid_ohlcv_fields.copy()
    args_02 = _valid_ohlcv_fields.copy()
    date = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    args_01["period_start"] = date - timedelta(seconds=1)
    args_02["period_start"] = date + timedelta(seconds=1)
    obj_1 = OHLCV(**args_01)
    obj_2 = OHLCV(**args_02)
    assert obj_1 < obj_2
    assert not (obj_1 > obj_2)

def test_lt__when_object_not_OHLCV__then_raises_NotImplemented(_valid_ohlcv_fields):
    obj_1 = OHLCV(**_valid_ohlcv_fields)
    args = _valid_ohlcv_fields.copy()
    with pytest.raises(TypeError):
        obj_1 < args

def test_lt__when_objects_too_differents__then_raises_NotImplemented(_valid_ohlcv_fields):
    obj_1 = OHLCV(**_valid_ohlcv_fields)
    args = _valid_ohlcv_fields.copy()
    args["ticker"] = "MSFT"
    obj_2 = OHLCV(**args)
    with pytest.raises(TypeError):
        obj_1 < obj_2

def test_frozen__when_attempt_mutation__then_raises_exception(_valid_ohlcv_fields):
    obj = OHLCV(**_valid_ohlcv_fields)
    with pytest.raises(FrozenInstanceError):
        obj.ticker = "MSFT"
