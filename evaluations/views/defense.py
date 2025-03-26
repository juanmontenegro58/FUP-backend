from rest_framework import viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.defense import (
    DefenseModelSerializer,
    DefenseListModelSerializer,
    DefenseDetailModelSerializer,
    DefenseRescheduleSerializer
)
from ..models import (
    Defense
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar sustentaciones",
        description="Devuelve una lista de todas las sustentaciones registrados.",
        tags = ['Sustentación']
    ),
    retrieve=extend_schema(
        summary="Obtener una sustentación",
        description="Obtiene los detalles de una sustentación específica por su ID.",
        tags = ['Sustentación']
    ),
    create=extend_schema(
        summary="Crear una nueva sustentación",
        description="Registra una nueva sustentación en el sistema.",
        tags = ['Sustentación']
    ),
    update=extend_schema(
        summary="Actualizar una sustentación",
        description="Actualiza los campos de una sustentación existente.",
        tags = ['Sustentación']
    ),
    
)
class DefenseViewSet(viewsets.ModelViewSet):

    queryset = Defense.objects.all()
    serializer_class = DefenseModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        serializers = {
            'list': DefenseListModelSerializer,
            'retrieve': DefenseDetailModelSerializer,
            'reschedule': DefenseRescheduleSerializer
        }
        return (
            serializers
            .get(
                self.action,
                super().get_serializer_class()
            )
        )
    
    @extend_schema(
        summary = 'Reprogramar sustentación',
        description = 'Reprograma la sustentación.',
        tags = ['Sustentación']
    )
    @action(detail = True, methods = ['post'], url_path = 'reschedule')
    def reschedule(self, request, pk = None):
        
        serializer = self.get_serializer_class()
        serializer.is_valid(raise_exception = True)