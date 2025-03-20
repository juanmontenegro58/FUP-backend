from django.core.exceptions import (
    ValidationError,
    PermissionDenied
)
from django.db import transaction
from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..models import (
    Agreement
)
from ..serializers.agreement import (
    AgreementCreateModelSerializer,
    AgreementDetailModelSerializer,
    AgreementDocumentUploadSerializer,
    AgreementAssignStudentSerializer
)
from ..serializers.document_agreement import (
    AgreementDocumentThroughModelSerializer
)
from ..controllers.agreement import (
    AgreementUploadDocumentController,
    AgreementAssignStudentController
)
from ..repositories.agreement import (
    AgreementRepository,
    AgreementDocumentThroughRepository
)
from core.validators.validator import (
    ValidatorRules
)
from programs.repositories.student import (
    StudentRepository
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar convenios",
        description="Devuelve una lista de todos los convenios registrados.",
        tags = ['Convenio']
    ),
    retrieve=extend_schema(
        summary="Obtener un convenio",
        description="Obtiene los detalles de un convenio específico por su ID.",
        tags = ['Convenio']
    ),
    create=extend_schema(
        summary="Crear un nuevo convenio",
        description="Registra un nuevo convenio en el sistema.",
        tags = ['Convenio']
    ),
    update=extend_schema(
        summary="Actualizar un convenio",
        description="Actualiza todos los campos de un convenio existente.",
        tags = ['Convenio']
    ),
    
)
class AgreementViewSet(viewsets.ModelViewSet):

    queryset = Agreement.objects.all()
    serializer_class = AgreementCreateModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AgreementDetailModelSerializer
        if self.action == 'upload_documents':
            return AgreementDocumentUploadSerializer
        if self.action == 'documents':
            return AgreementDocumentThroughModelSerializer
        if self.action == 'assign_student':
            return AgreementAssignStudentSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary = 'Listar documentos del convenio',
        description = 'Obtiene la lista de documentos asociados a un convenio específico.',
        responses = {200: AgreementDocumentThroughModelSerializer(many = True)},
        tags = ['Convenio']
    )
    @action(detail = True, methods = ['get'], url_path = 'documents')
    def documents(self, request, pk = None):
        repository = AgreementDocumentThroughRepository()
        queryset = repository.filter(agreement_id=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary = 'Cargar documentos del convenio',
        description = 'Permite la carga de multiples documentos asociados al convenio.',
        tags = ['Convenio']
    )
    @action(detail = True, methods = ['post'], url_path = 'documents/upload')
    def upload_documents(self, request, pk = None):
        """  
        Carga múltiples documentos para un convenio.
        """

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        data = {
            'agreement_id': pk,
            'files': serializer.validated_data['files'],
            'through_ids': serializer.validated_data['through_ids'],
            'user': request.user
        }
        try:
            with transaction.atomic():
                controller = AgreementUploadDocumentController(
                    raw_data = data,
                    repository = AgreementRepository(),
                    agreement_document_through = AgreementDocumentThroughRepository(),
                    validator = ValidatorRules()
                )
                controller.execute()
        except ValidationError as e:
            return Response(
                {'message': ' '.join(e.messages)},
                status = status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {'message': str(e)},
                status = status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {'message': 'Error interno, por favor intenta más tarde.'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {'message': 'Archivos subidos correctamente'},
            status = status.HTTP_200_OK
        )
    
    @extend_schema(
        summary = 'Asignación de estudiante',
        description = 'Permite la asignación de un estudiante al convenio',
        tags = ['Convenio']
    )
    @action(detail = True, methods = ['post'], url_path = 'assign-student')
    def assign_student(self, request, pk = None):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        
        data = serializer.data
        data['agreement'] = self.get_object()

        try:
            controller = AgreementAssignStudentController(
                raw_data = data,
                repository = StudentRepository(),
                validator = ValidatorRules()
            )
            controller.execute()
        except ValidationError as e:
            return Response(
                {'message': ' '.join(e.messages)},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'message': 'Error interno, por favor intenta más tarde.'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'Estudiante asignado correctamente',
        },
            status = status.HTTP_200_OK
        )