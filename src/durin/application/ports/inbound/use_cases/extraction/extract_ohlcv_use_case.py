from __future__ import annotations

from typing import Protocol

from .....use_cases.extraction.extract_ohlcv.extract_ohlcv_input_data import ExtractOHLCVInputData
from .....use_cases.extraction.extract_ohlcv.extract_ohlcv_output_data import ExtractOHLCVOutputData

class ExtractOHLCVUseCase(Protocol):

    def execute(self, input: ExtractOHLCVInputData) -> ExtractOHLCVOutputData:
        """Extract OHLCV data over a period from a source."""
        ...