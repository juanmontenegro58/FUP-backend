from rest_framework import viewsets
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