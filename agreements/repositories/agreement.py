from core.interfaces.repository import (
    RepositoryInterface
)

from ..models import (
    Agreement,
    AgreementDocumentThrough,
    AgreementStudentThrough,
    AgreementDocumentComment
)

class AgreementRepository(RepositoryInterface[Agreement]):

    def __init__(self):
        super().__init__(Agreement)

class AgreementDocumentThroughRepository(RepositoryInterface[AgreementDocumentThrough]):

    def __init__(self):
        super().__init__(AgreementDocumentThrough)

class AgreementStudentThroughRepository(RepositoryInterface[AgreementStudentThrough]):

    def __init__(self):
        super().__init__(AgreementStudentThrough)

class AgreementDocumentCommentRepository(RepositoryInterface[AgreementDocumentComment]):

    def __init__(self):
        super().__init__(AgreementDocumentComment)