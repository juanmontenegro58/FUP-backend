from django.core.exceptions import (
    PermissionDenied
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

from practices.serializers.internship_tracking import (
    InternshipTrackingModelSerializer
)
from ..serializers.practice import (
    PracticeModelSerializer,
    PracticeListModelSerializer,
    PracticeDetailModelSerializer,
    PracticeDocumentCreateSerializer
)
from ..models import (
    Practice
)
from ..repositories.internship_tracking import (
    InternshipTrackingRepository
)
from ..repositories.practice import (
    DocumentPracticeRepository
)
from core.constants.text import (
    NOT_PERMISSION
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar practicas",
        description="Devuelve una lista de todas las practicas registrados.",
        tags = ['Práctica']
    ),
    retrieve=extend_schema(
        summary="Obtener una práctica",
        description="Obtiene los detalles de una práctica específica por su ID.",
        tags = ['Práctica']
    ),
    create=extend_schema(
        summary="Crear una nueva práctica",
        description="Registra una nueva práctica en el sistema.",
        tags = ['Práctica']
    ),
    update=extend_schema(
        summary="Actualizar una práctica",
        description="Actualiza los campos de una práctica existente.",
        tags = ['Práctica']
    ),
    
)
class PracticeViewSet(viewsets.ModelViewSet):

    queryset = Practice.objects.all()
    serializer_class = PracticeModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        serializers = {
            'list': PracticeListModelSerializer,
            'retrieve': PracticeDetailModelSerializer,
            'internship_trackings': InternshipTrackingModelSerializer,
            'upload_documents': PracticeDocumentCreateSerializer
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
            'list': 'practices.view_practice',
            'retrieve': 'practices.view_practice',
            'create': 'practices.add_practice',
            'update': 'practices.change_practice',
            'upload_documents': 'practices.add_documentpractice'
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()
    
    @extend_schema(
        methods = ['get'],
        summary = 'Listar seguimientos de una práctica',
        description = 'Obtiene la lista de seguimientos asociados a una práctica específica.',
        responses = {200: InternshipTrackingModelSerializer(many = True)},
        tags = ['Práctica']
    )
    @extend_schema(
        methods = ['post'],
        summary = "Crear un nuevo registro de seguimiento a una práctica",
        description = "Registra un nuevo registro de seguimiento a una práctica en el sistema.",
        responses = {201: InternshipTrackingModelSerializer},
        tags = ['Práctica']
    )
    @action(detail = True, methods = ['get', 'post'], url_path = 'internship-trackings')
    def internship_trackings(self, request, pk = None):
        if request.method == 'GET':
            return self.handle_get_internship_trackings(request, pk)
        elif request.method == 'POST':
            serializer = self.get_serializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            serializer.save(
                practice_id = pk,
                created_by = request.user
            )
            return Response(serializer.data, status = status.HTTP_201_CREATED)

    def handle_get_internship_trackings(self, request, pk = None):
        repository = InternshipTrackingRepository()
        queryset = repository.filter(practice_id = pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @extend_schema(
        summary = 'Carga documentos a una práctica',
        description = 'Carga multiples documentos a una práctica específica.',
        responses = {200: InternshipTrackingModelSerializer(many = True)},
        tags = ['Práctica']
    )
    @action(detail = True, methods = ['post'], url_path = 'documents/upload')
    def upload_documents(self, request, pk = None):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        repository = DocumentPracticeRepository()
        data = serializer.validated_data

        for name, file in zip(data['names'], data['files']):
            data = {
                'name': name,
                'file': file,
                'uploaded_by': request.user,
                'practice_id': pk
            }
            repository.create(**data)
        return Response(
            {'message': 'Archivos subidos correctamente'},
            status = status.HTTP_200_OK
        )