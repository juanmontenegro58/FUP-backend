from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError
)
from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.practice import (
    PracticeModelSerializer,
    PracticeListModelSerializer,
    PracticeDetailModelSerializer
)
from ..models import (
    Practice
)
from core.validators.validator import (
    ValidatorRules
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar practicas",
        description="Devuelve una lista de todas las practicas registrados.",
        tags = ['Práctica']
    ),
    retrieve=extend_schema(
        summary="Obtener una práctica",
        description="Obtiene los detalles de una práctica específica por su ID.",
        tags = ['Práctica']
    ),
    create=extend_schema(
        summary="Crear una nueva práctica",
        description="Registra una nueva práctica en el sistema.",
        tags = ['Práctica']
    ),
    update=extend_schema(
        summary="Actualizar una práctica",
        description="Actualiza los campos de una práctica existente.",
        tags = ['Práctica']
    ),
    
)
class PracticeViewSet(viewsets.ModelViewSet):

    queryset = Practice.objects.all()
    serializer_class = PracticeModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        serializers = {
            'list': PracticeListModelSerializer,
            'retrieve': PracticeDetailModelSerializer,
        }
        return (
            serializers
            .get(
                self.action,
                super().get_serializer_class()
            )
        )