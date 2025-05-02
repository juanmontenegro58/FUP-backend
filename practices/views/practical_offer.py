from rest_framework import (
    viewsets
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..models import (
    PracticalOffer
)
from ..serializers.practical_offer import (
    PracticalOfferCreateModelSerializer,
    PracticalOfferListModelSerializer
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar ofertas practicas",
        description="Devuelve una lista de todas las practicas registrados.",
        tags = ['Oferta práctica']
    ),
    retrieve=extend_schema(
        summary="Obtener una Oferta práctica",
        description="Obtiene los detalles de una Oferta práctica específica por su ID.",
        tags = ['Oferta práctica']
    ),
    create=extend_schema(
        summary="Crear una nueva Oferta práctica",
        description="Registra una nueva Oferta práctica en el sistema.",
        tags = ['Oferta práctica']
    ),
    update=extend_schema(
        summary="Actualizar una Oferta práctica",
        description="Actualiza los campos de una Oferta práctica existente.",
        tags = ['Oferta práctica']
    ),
    
)
class PracticalOfferViewSet(viewsets.ModelViewSet):

    queryset = PracticalOffer.objects.all()
    serializer_class =PracticalOfferCreateModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        actions = {
            'list': PracticalOfferListModelSerializer
        }
        return actions.get(
            self.action,
            super().get_serializer_class()
        )