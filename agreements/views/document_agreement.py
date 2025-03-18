from rest_framework import viewsets

from ..serializers.document_agreement import (
    DocumentAgreementModelSerializer
)
from ..models import (
    DocumentAgreement
)

class DocumentAgreementViewSet(viewsets.ModelViewSet):
    
    queryset = DocumentAgreement.objects.all()
    serializer_class = DocumentAgreementModelSerializer
    http_method_names = ['get', 'post', 'put']