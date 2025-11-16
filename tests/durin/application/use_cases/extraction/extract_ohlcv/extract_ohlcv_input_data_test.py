from datetime import datetime, timedelta, timezone
import pytest

from durin.application import (
    ApplicationException,
    ExtractOHLCVInputData,
)

@pytest.fixture
def _valid_input_data_fields() -> ExtractOHLCVInputData:
    start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    end = datetime(2025, 12, 31, 9, 30, tzinfo=timezone.utc)
    return dict(
        source="Yahoo",
        ticker="AAPL",
        start=start,
        end=end,
        interval="1d",
    )

def test_init__when_valid_fields__then_create_ExtractOHLCVInputData_instance(_valid_input_data_fields):
    obj = ExtractOHLCVInputData(**_valid_input_data_fields)
    assert isinstance(obj, ExtractOHLCVInputData)

@pytest.mark.parametrize("field, bad_value", [
    ("source", 1),
    ("ticker", 2),
    ("start", "01/01/2025"),
    ("end", "31/12/2025"),
    ("interval", 3)
])
def test_init__when_type_invalid__then_raises_ApplicationException(_valid_input_data_fields, field, bad_value):
    args = _valid_input_data_fields.copy()
    args[field] = bad_value
    with pytest.raises(ApplicationException):
        ExtractOHLCVInputData(**args)

def test_init__when_timezone_not_valid__then_raises_ApplicationException(_valid_input_data_fields):
    args = _valid_input_data_fields.copy()
    datetime_without_timezone = datetime(2025, 1, 1, 9, 30)
    args["start"] = datetime_without_timezone
    with pytest.raises(ApplicationException):
        ExtractOHLCVInputData(**args)

def test_init__when_dates_inconsistent__then_raises_ApplicationException(_valid_input_data_fields):
    args = _valid_input_data_fields.copy()
    date = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    args["start"] = date + timedelta(seconds=1)
    args["end"] = date - timedelta(seconds=1)
    with pytest.raises(ApplicationException):
        ExtractOHLCVInputData(**args)