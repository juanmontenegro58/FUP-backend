from django.core.exceptions import (
    PermissionDenied,
    ObjectDoesNotExist
)
from rest_framework.views import APIView
from rest_framework import (
    viewsets,
    status
)
from rest_framework.response import (
    Response
)
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view
)

from ..serializers.document_agreement import (
    DocumentAgreementModelSerializer
)
from ..models import (
    DocumentAgreement
)
from ..repositories.document import (
    DocumentAgreementRepository
)
from core.constants.text import (
    NOT_PERMISSION
)
from core.decorators import (
    permission_required
)

class CustomPageDocuments(PageNumberPagination):
    page_size = 30

@extend_schema_view(
    list=extend_schema(
        summary="Listar documentos",
        description="Devuelve una lista de todos los documentos registrados.",
        tags = ['Documento']
    ),
    retrieve=extend_schema(
        summary="Obtener un documento",
        description="Obtiene los detalles de un documento específico por su ID.",
        tags = ['Documento']
    ),
    create=extend_schema(
        summary="Crear un nuevo documento",
        description="Registra un nuevo documento en el sistema.",
        tags = ['Documento']
    ),
    update=extend_schema(
        summary="Actualizar un documento",
        description="Actualiza todos los campos de un documento existente.",
        tags = ['Documento']
    ),
    
)
class DocumentAgreementViewSet(viewsets.ModelViewSet):
    
    queryset = DocumentAgreement.objects.all()
    serializer_class = DocumentAgreementModelSerializer
    http_method_names = ['get', 'post', 'put']
    pagination_class = CustomPageDocuments
    filterset_fields = [
        'is_active'
    ]

    def get_permissions(self):
        action_permissions = {
            'list': 'agreements.view_documentagreement',
            'retrieve': 'agreements.view_documentagreement',
            'create': 'agreements.add_documentagreement',
            'update': 'agreements.change_documentagreement',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()
    
@extend_schema_view(
    post=extend_schema(
        summary="Cambiar estado del documento",
        description="Intercambia el estado del documento `is_active` entre True y False.",
        tags = ['Documento']
    ),
)
class ToggleStatusDocumentAgreementView(APIView):

    serializer_class = None

    @permission_required('agreements.toggle_status_document')
    def post(self, request, document_id):
        doc_repo = DocumentAgreementRepository()
        try:
            document: DocumentAgreement = doc_repo.get_by_id(obj_id = document_id)
            document.is_active = not document.is_active
            document.save()
        except ObjectDoesNotExist as e:
            return Response({'message': str(e)}, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'message': 'Error interno, por favor intenta más tarde.'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(status = status.HTTP_200_OK)