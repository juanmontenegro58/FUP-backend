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


class ControllerInterface(ABC):
    def __init__(
        self, 
        raw_data: Dict[str, Any], 
        repository: RepositoryInterface
    ):
        self.raw_data = raw_data
        self.repository = repository

    @abstractmethod
    def execute(self) -> Any:
        """Método abstracto que cada controlador debe implementar."""
        raise NOT_IMPLEMENTED_ERROR
