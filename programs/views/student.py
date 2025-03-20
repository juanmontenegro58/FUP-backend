from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.student import (
    StudentModelSerializer
)
from ..models import (
    Student
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