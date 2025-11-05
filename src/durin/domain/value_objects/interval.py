from enum import Enum

class Interval(Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"

    @classmethod
    def from_str_to_enum(cls, value: str):
        try:
            return cls(value)
        except ValueError:
            return None