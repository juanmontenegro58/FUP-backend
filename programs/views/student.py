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

from ..serializers.student import (
    StudentModelSerializer,
    StudentListModelSerializer,
    StudentCreateModelSerializer
)
from ..models import (
    Student
)
from core.constants.text import (
    NOT_PERMISSION
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar estudiantes",
        description="Devuelve una lista de todos los estudiantes registrados.",
        tags = ['Estudiante']
    ),
    retrieve=extend_schema(
        summary="Obtener un estudiante",
        description="Obtiene los detalles de un estudiante específico por su ID.",
        tags = ['Estudiante']
    ),
    create=extend_schema(
        summary="Crear una nuevo estudiante",
        description="Registra una nuevo estudiante en el sistema.",
        tags = ['Estudiante']
    ),
    update=extend_schema(
        summary="Actualizar un estudiante",
        description="Actualiza los campos de un estudiante existente.",
        tags = ['Estudiante']
    ),
    
)
class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    http_method_names = ['get', 'post', 'put']
    search_fields = ['full_name', 'code', 'document_number']

    def get_serializer_class(self):
        actions = {
            'list': StudentListModelSerializer,
            'create': StudentCreateModelSerializer,
            'update': StudentCreateModelSerializer,
            'retrieve': StudentCreateModelSerializer
        }
        return actions.get(
            self.action,
            super().get_serializer_class()
        )
    
    def get_permissions(self):
        action_permissions = {
            'list': 'programs.view_student',
            'retrieve': 'programs.view_student',
            'create': 'programs.create_student',
            'update': 'programs.change_student',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()