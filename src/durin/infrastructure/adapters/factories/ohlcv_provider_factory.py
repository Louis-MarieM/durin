from typing import Any, Mapping, Optional, Protocol

from ..providers.yahoo_ohlcv_provider import YahooOHLCVProvider
from ...exceptions.infrastructure_exceptions import InfrastructureException
from durin.domain import Source

_PROVIDER_MAP: dict[Source, type] = {
    Source.YAHOO: YahooOHLCVProvider,
}

class OHLCVProviderFactory():

    def create(self, source: str, params: Optional[Mapping[str, Any]] = None) -> object:
        try:
            validated_source = Source(source)
            provider_class = _PROVIDER_MAP.get(validated_source)

            if provider_class is None:
                raise InfrastructureException("Unknown provider.", meta={"source": source})
            
            return provider_class(**(params or {}))
        except Exception as exception:
            raise InfrastructureException("Failed to create a OHLCV provider.", meta={"source": source, "params": params})
