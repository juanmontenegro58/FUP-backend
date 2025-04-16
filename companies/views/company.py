from rest_framework import (
    viewsets,
    filters
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.company import (
    CompanyModelSerializer,
    CompanyDetailSerializer
)
from ..models import (
    Company
)
from ..filters.company import (
    CompanyFilter
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar empresas",
        description="Devuelve una lista de todos los empresas registradas.",
        tags = ['Empresa']
    ),
    retrieve=extend_schema(
        summary="Obtener una empresa",
        description="Obtiene los detalles de una empresa específica por su ID.",
        tags = ['Empresa']
    ),
    create=extend_schema(
        summary="Crear una nueva empresa",
        description="Registra una nueva empresa en el sistema.",
        tags = ['Empresa']
    ),
    update=extend_schema(
        summary="Actualizar una empresa",
        description="Actualiza los campos de una empresa existente.",
        tags = ['Empresa']
    ),
    
)
class CompanyViewSet(viewsets.ModelViewSet):
    
    serializer_class = CompanyModelSerializer
    queryset = Company.objects.all()
    http_method_names = ['get', 'post', 'put']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'nui']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanyModelSerializer