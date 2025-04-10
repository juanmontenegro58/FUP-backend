from core.interfaces.repository import RepositoryInterface

from ..models import (
    InternshipTracking
)

class InternshipTrackingRepository(RepositoryInterface[InternshipTracking]):

    def __init__(self):
        super().__init__(InternshipTracking)