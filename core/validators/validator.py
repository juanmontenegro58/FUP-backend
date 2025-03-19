from typing import (
    List,
    Dict,
    Any
)

from ..interfaces.validator import (
    ValidatorInterface
)

class ValidatorRules:

    def __init__(self):
        self.rules: List[ValidatorInterface] = []

    def add_rules(self, rules: List[ValidatorInterface]) -> None:
        self.rules += rules

    def validate(self, data: Dict[str, Any]) -> None:
        for rule in self.rules:
            rule.validate(data = data)