from core.interfaces.repository import RepositoryInterface

from ..models import PracticalOffer

class PracticalOfferRepository(RepositoryInterface[PracticalOffer]):

    def __init__(self):
        super().__init__(PracticalOffer)