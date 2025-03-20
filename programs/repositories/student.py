from core.interfaces.repository import (
    RepositoryInterface
)

from ..models import (
    Student
)

class StudentRepository(RepositoryInterface[Student]):

    def __init__(self):
        super().__init__(Student)