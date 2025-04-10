from core.interfaces.repository import RepositoryInterface

from ..models import (
    DocumentPractice,
    Practice
)

class DocumentPracticeRepository(RepositoryInterface[DocumentPractice]):
    def __init__(self):
        super().__init__(DocumentPractice)