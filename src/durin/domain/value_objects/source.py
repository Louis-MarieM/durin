from enum import Enum

class Source(Enum):
    YAHOO = "Yahoo"
    BINANCE = "Binance"
    QUANDL = "Quandl"
    TWITTER = "Twitter"
    NEWSAPI = "NewsAPI"
    OCR = "OCR"

    @classmethod
    def from_str_to_enum(cls, value: str):
        try:
            return cls(value)
        except ValueError:
            return None