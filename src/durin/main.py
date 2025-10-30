from datetime import datetime, timezone

from durin.config.logger import logger
from durin.infrastructure import YahooOHLCVProvider, InfrastructureException


def run():
    yahooOHLCVProvider = YahooOHLCVProvider()
    yahooOHLCVDTO = yahooOHLCVProvider.fetch("AAPL", datetime(2024, 1, 1, 9, 30, tzinfo=timezone.utc), datetime(2024, 12, 31, 9, 30, tzinfo=timezone.utc), "1d")

    dto_save = []
    for dto in yahooOHLCVDTO:
        dto_save.append(dto)
        logger.info(dto_save[-1]) 
    logger.info(len(dto_save))
