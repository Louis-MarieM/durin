from datetime import datetime, timezone

from durin.config.logger import logger
from durin.infrastructure import OHLCVProviderFactory


def run():
    ohlcv_provider_factory = OHLCVProviderFactory()
    yahoo_ohlcv_provider = ohlcv_provider_factory.create("Yahoo", {"timeout": 29})
    yahoo_ohlcv = yahoo_ohlcv_provider.fetch("AAPL", datetime(2024, 1, 1, 9, 30, tzinfo=timezone.utc), datetime(2024, 12, 31, 9, 30, tzinfo=timezone.utc), "1d")

    # Tests ohlcv provider
    ohlcv_save = []
    for ohlcv in yahoo_ohlcv:
        ohlcv_save.append(ohlcv)
        logger.info(ohlcv_save[-1]) 
    logger.info(len(ohlcv_save))

    # Tests provider factory
    logger.info(yahoo_ohlcv_provider.timeout)
