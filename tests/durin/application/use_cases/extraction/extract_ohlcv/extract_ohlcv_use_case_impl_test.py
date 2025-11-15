from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import Mock
import copy, pytest

from durin.application import (
    ApplicationException,
    ExtractOHLCVInputData,
    ExtractOHLCVOutputData,
    ExtractOHLCVUseCaseImpl,
)
from durin.domain import (
    Currency, 
    Interval, 
    OHLCV, 
    Source, 
)

@pytest.fixture
def _valid_input_data_fields() -> ExtractOHLCVInputData:
    start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    end = datetime(2024, 12, 31, 9, 30, tzinfo=timezone.utc)
    return dict(
        source="Yahoo",
        ticker="AAPL",
        start=start,
        end=end,
        interval="1d",
    )

@pytest.fixture
def _ohlcv_iteratable() -> dict:
    start = datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
    fields = dict(
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
    ohlcv_1 = OHLCV(**fields)
    fields["ticker"] = "MSFT"
    ohlcv_2 = OHLCV(**fields)
    return(iter([ohlcv_1, ohlcv_2]))

def test_execute__when_valid_input__then_returns_OHLCV_list(_valid_input_data_fields, _ohlcv_iteratable):
    input_data = ExtractOHLCVInputData(**_valid_input_data_fields)

    provider_mock = Mock()
    provider_mock.fetch.return_value = _ohlcv_iteratable
    provider_factory_mock = Mock()
    provider_factory_mock.create.return_value = provider_mock

    extractor = ExtractOHLCVUseCaseImpl(provider_factory_mock)
    result = extractor.execute(input_data)

    assert isinstance(result, ExtractOHLCVOutputData)
    assert result.ohlcv_list is _ohlcv_iteratable

def test_execute__when_invalid_source__then_raises_ApplicationException(_valid_input_data_fields):
    args = _valid_input_data_fields.copy()
    args["source"] = "WrongSource"
    input_data = ExtractOHLCVInputData(**args)

    provider_factory_mock = Mock()
    provider_factory_mock.create.side_effect = ApplicationException("Unknown provider.", meta={"source": input_data.source})

    extractor = ExtractOHLCVUseCaseImpl(provider_factory_mock)
    with pytest.raises(ApplicationException):
        extractor.execute(input_data)

def test_execute__when_invalid_provider_input__then_raises_ApplicationException(_valid_input_data_fields):
    args = _valid_input_data_fields.copy()
    args["ticker"] = "WrongTicker"
    input_data = ExtractOHLCVInputData(**args)

    provider_mock = Mock()
    provider_mock.fetch.side_effect = ApplicationException("Yahoo finance service is unreachable or in error.", meta={"ticker": input_data.ticker, "start": input_data.start, "end": input_data.end, "interval": input_data.interval, "exception": ApplicationException("Mother exception")})
    provider_factory_mock = Mock()
    provider_factory_mock.create.return_value = provider_mock

    extractor = ExtractOHLCVUseCaseImpl(provider_factory_mock)
    with pytest.raises(ApplicationException):
        extractor.execute(input_data)

def test_execute__when_unknown_error__then_raises_ApplicationException(_valid_input_data_fields):
    args = _valid_input_data_fields.copy()
    args["ticker"] = "WrongTicker"
    input_data = ExtractOHLCVInputData(**args)

    provider_mock = Mock()
    provider_mock.fetch.side_effect = Exception("Service unreachable.")
    provider_factory_mock = Mock()
    provider_factory_mock.create.return_value = provider_mock

    extractor = ExtractOHLCVUseCaseImpl(provider_factory_mock)
    with pytest.raises(ApplicationException):
        extractor.execute(input_data)