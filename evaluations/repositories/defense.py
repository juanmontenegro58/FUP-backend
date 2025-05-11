from core.interfaces.repository import (
    RepositoryInterface
)

from ..models import (
    Defense,
    DefenseComment,
    DocumentDefense
)

class DefenseRepository(RepositoryInterface[Defense]):

    def __init__(self):
        super().__init__(Defense)

class DefenseCommentRepository(RepositoryInterface[DefenseComment]):

    def __init__(self):
        super().__init__(DefenseComment)

class DocumentDefenseRepository(RepositoryInterface[DocumentDefense]):

    def __init__(self):
        super().__init__(DocumentDefense)