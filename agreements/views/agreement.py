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

from ..models import (
    Agreement
)
from ..serializers.agreement import (
    AgreementCreateModelSerializer,
    AgreementDetailModelSerializer,
    AgreementDocumentUploadSerializer
)
from ..serializers.document_agreement import (
    AgreementDocumentThroughModelSerializer
)
from ..controllers.agreement import (
    AgreementUploadDocumentController
)
from ..repositories.agreement import (
    AgreementRepository,
    AgreementDocumentThroughRepository
)
from core.validators.validator import (
    ValidatorRules
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
        return super().get_serializer_class()

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
            status = status.HTTP_201_CREATED
        )