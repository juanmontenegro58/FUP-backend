from core.interfaces.repository import (
    RepositoryInterface
)

from ..models import (
    Agreement,
    AgreementDocumentThrough
)

class AgreementRepository(RepositoryInterface[Agreement]):

    def __init__(self):
        super().__init__(Agreement)

class AgreementDocumentThroughRepository(RepositoryInterface[AgreementDocumentThrough]):

    def __init__(self):
        super().__init__(AgreementDocumentThrough)