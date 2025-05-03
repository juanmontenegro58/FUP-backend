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

from ..serializers.teacher import (
    TeacherModelSerializer
)
from ..models import (
    Teacher
)
from core.constants.text import (
    NOT_PERMISSION
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar docentes",
        description="Devuelve una lista de todos los docentes registrados.",
        tags = ['Docente']
    ),
    retrieve=extend_schema(
        summary="Obtener un docente",
        description="Obtiene los detalles de un docente específico por su ID.",
        tags = ['Docente']
    ),
    create=extend_schema(
        summary="Crear una nuevo docente",
        description="Registra una nuevo docente en el sistema.",
        tags = ['Docente']
    ),
    update=extend_schema(
        summary="Actualizar un docente",
        description="Actualiza los campos de un docente existente.",
        tags = ['Docente']
    ),
    
)
class TeacherViewSet(viewsets.ModelViewSet):

    queryset = Teacher.objects.all()
    serializer_class = TeacherModelSerializer
    http_method_names = ['get', 'post', 'put']
    search_fields = ['full_name', 'document_number']

    def get_permissions(self):
        action_permissions = {
            'list': 'evaluations.view_teacher',
            'retrieve': 'evaluations.view_teacher',
            'create': 'evaluations.add_teacher',
            'update': 'evaluations.change_teacher',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()