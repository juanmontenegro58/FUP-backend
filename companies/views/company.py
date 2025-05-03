from django.core.exceptions import (
    PermissionDenied
)
from rest_framework import (
    viewsets,
)
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
from core.constants.text import (
    NOT_PERMISSION
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
    search_fields = ['name', 'nui']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanyModelSerializer
    
    def get_permissions(self):
        action_permissions = {
            'list': 'companies.view_company',
            'retrieve': 'companies.view_company',
            'create': 'companies.add_company',
            'update': 'companies.change_company',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()