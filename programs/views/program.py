from rest_framework import (
    viewsets,
    filters
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.program import (
    ProgramModelSerializer
)
from ..models import (
    Program
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar programas",
        description="Devuelve una lista de todos los programas registrados.",
        tags = ['Programa']
    ),
    retrieve=extend_schema(
        summary="Obtener un programa",
        description="Obtiene los detalles de un programa específico por su ID.",
        tags = ['Programa']
    ),
    create=extend_schema(
        summary="Crear una nuevo programa",
        description="Registra una nuevo programa en el sistema.",
        tags = ['Programa']
    ),
    update=extend_schema(
        summary="Actualizar un programa",
        description="Actualiza los campos de un programa existente.",
        tags = ['Programa']
    ),
    
)
class ProgramViewSet(viewsets.ModelViewSet):

    queryset = Program.objects.all()
    serializer_class = ProgramModelSerializer
    http_method_names = ['get', 'post', 'put']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']