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

from ..serializers.defense import (
    DefenseModelSerializer,
    DefenseListModelSerializer,
    DefenseDetailModelSerializer,
    DefenseRescheduleSerializer,
    DefenseCommentModelSerializer
)
from ..models import (
    Defense
)
from ..controllers.defense import (
    RescheduleDefenseController
)
from ..repositories.defense import (
    DefenseRepository,
    DefenseCommentRepository
)
from core.validators.validator import (
    ValidatorRules
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
            'comments': DefenseCommentModelSerializer,
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
        
        serializer = DefenseRescheduleSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        data = {
            **serializer.data,
            'user': request.user,
            'defense_id': pk
        }

        repositories = {
            'defense': DefenseRepository(),
            'defense_comment': DefenseCommentRepository()
        }

        try:
            controller = RescheduleDefenseController(
                raw_data = data,
                repositories = repositories,
                validator = ValidatorRules()
            )
            controller.execute()
        except ObjectDoesNotExist as e:
            return Response(
                {'message': str(e)},
                status = status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'message': e.message},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {'message': 'Error interno, por favor intenta más tarde.'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({'message': 'Reprogramación completada'}, status = status.HTTP_200_OK)
    
    @extend_schema(
        summary = 'Comentarios de sustentación',
        description = 'Lista los comentarios de una sustentación',
        tags = ['sustentación']
    )
    @action(detail = True, methods = ['get'], url_path = 'comments')
    def comments(self, request, pk = None):
        repository = DefenseCommentRepository()
        queryset = repository.filter(defense__id = pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)