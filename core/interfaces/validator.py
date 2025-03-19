from typing import (
    Dict,
    Any
)
from abc import (
    abstractmethod,
    ABC
)

from ..constants.text import (
    NOT_IMPLEMENTED_ERROR
)

class ValidatorInterface(ABC):

    @staticmethod
    @abstractmethod
    def validate(data: Dict[str, Any]):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)