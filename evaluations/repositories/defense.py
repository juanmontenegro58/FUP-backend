from core.interfaces.repository import (
    RepositoryInterface
)

from ..models import (
    Defense,
    DefenseComment
)

class DefenseRepository(RepositoryInterface[Defense]):

    def __init__(self):
        super().__init__(Defense)

class DefenseCommentRepository(RepositoryInterface[DefenseComment]):

    def __init__(self):
        super().__init__(DefenseComment)