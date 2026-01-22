import re
from dataclasses import dataclass

from ..exceptions.domain_exceptions import ValidationException

@dataclass(frozen=True)
class CronExpression:
    """Value object to represents valid cron expression"""
    
    value: str
    
    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValidationException(f"Invalid cron expression: {self.value}")
    
    @staticmethod
    def _is_valid(cron_expression: str) -> bool:
        parts = cron_expression.strip().split()
        
        if len(parts) != 5:
            return False
        
        patterns = [
            r'^(\*|[0-5]?[0-9]|(\*\/[0-9]+)|([0-5]?[0-9]-[0-5]?[0-9])(,[0-5]?[0-9])*)$',  # minute
            r'^(\*|[0-1]?[0-9]|2[0-3]|(\*\/[0-9]+)|([0-1]?[0-9]-2[0-3])(,[0-2]?[0-9])*)$',  # heure
            r'^(\*|[1-2]?[0-9]|3[0-1]|(\*\/[0-9]+)|([1-2]?[0-9]-3[0-1])(,[1-3]?[0-9])*)$',  # jour
            r'^(\*|[1-9]|1[0-2]|(\*\/[0-9]+)|([1-9]-1[0-2])(,[1]?[0-9])*)$',                # mois
            r'^(\*|[0-6]|(\*\/[0-9]+)|([0-6]-[0-6])(,[0-6])*)$'                             # jour semaine
        ]
        
        return all(re.match(pattern, part) is not None for pattern, part in zip(patterns, parts))
    
    def __str__(self) -> str:
        return self.value