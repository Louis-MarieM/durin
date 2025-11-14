from __future__ import annotations

from ....ports.outbound.factories.provider_factory import ProviderFactory
from ....exceptions.application_exceptions import ApplicationException
from .extract_ohlcv_input_data import ExtractOHLCVInputData
from .extract_ohlcv_output_data import ExtractOHLCVOutputData

class ExtractOHLCVUseCaseImpl():

    def __init__(self, provider_factory: ProviderFactory):
        self.provider_factory = provider_factory

    def execute(self, input: ExtractOHLCVInputData) -> ExtractOHLCVOutputData:
        try:
            provider = self.provider_factory.create(input.source)
            fetched_ohlcv = provider.fetch(input.ticker, input.start, input.end, input.interval)
            return ExtractOHLCVOutputData(ohlcv_list=fetched_ohlcv)
        except ApplicationException as application_exception:
            raise ApplicationException("Failed to fetch OHLCV data.", meta={"InputData": input, "exception": application_exception})
        except Exception as exception:
            raise ApplicationException("Unknown error.", meta={"InputData": input, "exception": exception})