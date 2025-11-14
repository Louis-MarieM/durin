from datetime import datetime, timezone

from durin.application import ExtractOHLCVInputData, ExtractOHLCVUseCaseImpl
from durin.config.logger import logger
from durin.infrastructure import OHLCVProviderFactory


def run():
    ohlcv_provider_factory = OHLCVProviderFactory()
    extracter = ExtractOHLCVUseCaseImpl(ohlcv_provider_factory)

    extracter_input = ExtractOHLCVInputData(
        source="Yahoo",
        ticker="AAPL",
        start=datetime(2024, 1, 1, 9, 30, tzinfo=timezone.utc),
        end=datetime(2024, 12, 31, 9, 30, tzinfo=timezone.utc),
        interval="1d",
    )

    extracter_output = extracter.execute(extracter_input)
    yahoo_ohlcv = extracter_output.ohlcv_list

    # Tests ohlcv provider
    ohlcv_save = []
    for ohlcv in yahoo_ohlcv:
        ohlcv_save.append(ohlcv)
        logger.info(ohlcv_save[-1]) 
    logger.info(len(ohlcv_save))
