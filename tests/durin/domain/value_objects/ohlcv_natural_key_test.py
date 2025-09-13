from datetime import datetime, timezone, timedelta
import pytest

from durin.domain import compute_natural_key, DomainException

@pytest.fixture
def _valid_key_fields() -> dict:
    period_start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    return dict(
        ticker="AAPL",
        interval="1m",
        period_start=period_start
    )

@pytest.mark.parametrize("field, bad_value", [
    ("ticker", "  aapl  "),
    ("interval", " 1M "),
    ("period_start", datetime(2025, 1, 1, 9, 30, 0, 123456))
])
def test_compute_natural_key__when_field_to_normalize__then_compute_normalized_key(_valid_key_fields, field, bad_value):
    args = {**_valid_key_fields}
    args[field] = bad_value
    key = compute_natural_key(**args)
    assert key == "AAPL|1m|2025-01-01T09:30:00Z"

@pytest.mark.parametrize("field, bad_value", [
    ("ticker", None),
    ("interval", None),
    ("period_start", None)
])
def test_compute_natural_key__when_none_field__then_raises_(_valid_key_fields, field, bad_value):
    args = {**_valid_key_fields}
    args[field] = bad_value
    with pytest.raises(DomainException):
       compute_natural_key(**args)

def test_compute_natural_key__when_not_utc_datetime__then_convert_to_utc(_valid_key_fields):
    tz_plus2 = timezone(timedelta(hours=2))
    tz_plus2_datetime = datetime(2025, 1, 1, 11, 30, tzinfo=tz_plus2)
    args = {**_valid_key_fields}
    args["period_start"] = tz_plus2_datetime
    key = compute_natural_key(**args)
    assert key == "AAPL|1m|2025-01-01T09:30:00Z"

def test_compute_natural_key__when_same_fields__then_compute_same_key(_valid_key_fields):
    key_1 = compute_natural_key(**_valid_key_fields)
    key_2 = compute_natural_key(**_valid_key_fields)
    assert key_1 == key_2