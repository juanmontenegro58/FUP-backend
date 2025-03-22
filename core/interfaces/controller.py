from abc import (
    ABC, 
    abstractmethod
)
from typing import (
    Any, 
    Dict
)
from .repository import RepositoryInterface
from ..constants.text import (
    NOT_IMPLEMENTED_ERROR
)
from ..validators.validator import ValidatorRules


class ControllerInterface(ABC):
    def __init__(
        self, 
        raw_data: Dict[str, Any], 
        repository: RepositoryInterface,
        validator: ValidatorRules
    ):
        self.raw_data = raw_data
        self.repository = repository
        self.validator = validator

    @abstractmethod
    def execute(self) -> Any:
        """Método abstracto que cada controlador debe implementar."""
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)

class ControllerMultiRepositoryInterface(ABC):

    def __init__(
        self,
        raw_data: Dict[str, Any],
        validator: ValidatorRules,
        repositories: Dict[str, RepositoryInterface]
    ):
        self.raw_data = raw_data
        self.validator = validator
        self.repositories = repositories

    @abstractmethod
    def execute(self) -> Any:
        """Método abstracto que cada controlador debe implementar."""
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)