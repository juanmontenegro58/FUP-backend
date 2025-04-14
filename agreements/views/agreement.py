from django.core.exceptions import (
    ValidationError,
    PermissionDenied,
    ObjectDoesNotExist
)
from django.db import transaction
from rest_framework import (
    viewsets,
    status,
    filters
)
from rest_framework.views import (
    APIView
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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
    AgreementAssignStudentSerializer,
    AgreementDocumentChangeStateSerializer
)
from ..serializers.document_agreement import (
    AgreementDocumentThroughModelSerializer
)
from ..controllers.agreement import (
    AgreementUploadDocumentController,
    AgreementAssignStudentController,
    UpdateAgreementDocumentStatusController
)
from ..repositories.agreement import (
    AgreementRepository,
    AgreementDocumentThroughRepository,
    AgreementDocumentCommentRepository
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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['company__name', 'name', 'company__nui']

    def get_serializer_class(self):
        serializers = {
            'retrieve': AgreementDetailModelSerializer,
            'upload_documents': AgreementDocumentUploadSerializer,
            'documents': AgreementDocumentThroughModelSerializer,
            'assign_student': AgreementAssignStudentSerializer
        }
        return (
            serializers
            .get(
                self.action,
                super().get_serializer_class()
            )
        )

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
    
class UpdateAgreementDocumentStatusView(APIView):

    serializer_class = AgreementDocumentChangeStateSerializer

    @extend_schema(
        summary = 'Cambiar estado del documento',
        description = 'Permite cambiar el estado del documento.',
        tags = ['Convenio']
    )
    def post(self, request, agreement_id, document_agreement_id):

        serializer = AgreementDocumentChangeStateSerializer(
            data = request.data
        )
        serializer.is_valid(raise_exception = True)

        data = {
            **serializer.data,
            'user': request.user,
            'agreement_id': agreement_id,
            'document_agreement_id': document_agreement_id
        }

        repositories = {
            'agreement': AgreementRepository(),
            'agreement_document': AgreementDocumentThroughRepository(),
            'comment': AgreementDocumentCommentRepository()
        }

        try:
            controller = UpdateAgreementDocumentStatusController(
                raw_data = data,
                validator = ValidatorRules(),
                repositories = repositories
            )
            controller.execute()
        except ValidationError as e:
            return Response(
                {'message': ' '.join(e.messages)},
                status = status.HTTP_400_BAD_REQUEST
            )
        except (PermissionDenied, ObjectDoesNotExist) as e:
            return Response(
                {'message': str(e)},
                status = status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            import traceback
            print(traceback.print_exc())
            return Response(
                {'message': 'Error interno, por favor intenta más tarde.'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({'message': 'Estado del documento actualizado con éxito.'}, status = status.HTTP_200_OK)