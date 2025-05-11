from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
    PermissionDenied
)
from django.db.transaction import (
    atomic
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
    DefenseCommentModelSerializer,
    DefenseCommentSerializer,
    DefenseFinishSerializer
)
from ..models import (
    Defense
)
from ..controllers.defense import (
    RescheduleDefenseController
)
from ..repositories.defense import (
    DefenseRepository,
    DefenseCommentRepository,
    DocumentDefenseRepository
)
from core.validators.validator import (
    ValidatorRules
)
from core.constants.text import (
    NOT_PERMISSION
)
from ..enums import (
    DefenseStatusEnum
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

    queryset = Defense.objects.prefetch_related('students')
    serializer_class = DefenseModelSerializer
    http_method_names = ['get', 'post', 'put']
    search_fields = [
        'students__full_name',
        'students__document_number',
        'students__code',
    ]

    def get_serializer_class(self):
        serializers = {
            'list': DefenseListModelSerializer,
            'retrieve': DefenseDetailModelSerializer,
            'comments': DefenseCommentModelSerializer,
            'reschedule': DefenseRescheduleSerializer,
            'finish': DefenseFinishSerializer
        }
        return (
            serializers
            .get(
                self.action,
                super().get_serializer_class()
            )
        )
    
    def get_permissions(self):
        action_permissions = {
            'list': 'evaluations.view_defense',
            'retrieve': 'evaluations.view_defense',
            'create': 'evaluations.add_defense',
            'update': 'evaluations.change_defense',
            'reschedule': 'evaluations.change_defense',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()
    
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
        methods = ['get'],
        summary = 'Comentarios de sustentación',
        description = 'Lista los comentarios de una sustentación',
        tags = ['Sustentación']
    )
    @extend_schema(
        methods = ['post'],
        summary = 'Comentarios de sustentación',
        description = 'Crea un comentario a una sustentación',
        tags = ['Sustentación'],
        request = DefenseCommentSerializer,
        responses = {
            201: DefenseCommentModelSerializer
        }
    )
    @action(detail = True, methods = ['get', 'post'], url_path = 'comments')
    def comments(self, request, pk = None):
        if request.method == 'GET':
            return self.handle_get_comments(request, pk)
        if request.method == 'POST':
            return self.handle_post_comments(request, pk)
    
    @extend_schema(
        methods = ['post'],
        summary = 'Finalizar sustentación',
        description = 'Cierra o finaliza una sustentación',
        tags = ['Sustentación'],
        request = DefenseFinishSerializer,
        responses = {
            204: None
        }
    )
    @action(detail = True, methods = ['post'], url_path = 'finish')
    def finish(self, request, pk = None):
        
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        defense_repository = DefenseRepository()
        document_def_repository = DocumentDefenseRepository()
        try:
            defense: Defense = defense_repository.get_by_id(obj_id = pk)
            document = document_def_repository.filter(name__iexact = 'acta de sustentación', defense = defense)
            with atomic():
                if document.exists():
                    document.delete()
                document_def_repository.create(
                    name = 'Acta de sustentación',
                    file = serializer.validated_data['supporting_document'],
                    defense_id = pk,
                    uploaded_by = request.user
                )
                defense.status = DefenseStatusEnum.COMPLETADA.value
                defense.result = serializer.data['result']
                defense.save()
        except Exception as e:
            return Response({'detail': 'Error procesando la información'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status = status.HTTP_204_NO_CONTENT)
    
    def handle_get_comments(self, request, pk = None):
        repository = DefenseCommentRepository()
        queryset = repository.filter(defense__id = pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def handle_post_comments(self, request, pk = None):
        repository_defense = DefenseRepository()
        repository_defense_comment = DefenseCommentRepository()

        serializer = DefenseCommentSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        

        data = {
            'created_by': request.user,
            'defense': repository_defense.get_by_id(obj_id = pk),
            **serializer.data
        }

        comment = repository_defense_comment.create(**data)

        return Response(DefenseCommentModelSerializer(comment).data, status = status.HTTP_201_CREATED)