from core.interfaces.repository import RepositoryInterface

from ..models import (
    DocumentAgreement
)

class DocumentAgreementRepository(RepositoryInterface[DocumentAgreement]):
    def __init__(self):
        super().__init__(DocumentAgreement)