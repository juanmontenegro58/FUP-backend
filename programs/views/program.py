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

from ..serializers.program import (
    ProgramModelSerializer
)
from ..models import (
    Program
)
from core.constants.text import (
    NOT_PERMISSION
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
    search_fields = ['name']

    def get_permissions(self):
        action_permissions = {
            'list': 'programs.view_program',
            'retrieve': 'programs.view_program',
            'create': 'programs.add_program',
            'update': 'programs.change_program',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()