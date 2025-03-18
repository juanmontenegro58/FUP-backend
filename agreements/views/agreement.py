from rest_framework import viewsets

from ..models import (
    Agreement
)
from ..serializers.agreement import (
    AgreementCreateModelSerializer,
    AgreementDetailModelSerializer
)

class AgreementViewSet(viewsets.ModelViewSet):

    queryset = Agreement.objects.all()
    serializer_class = AgreementCreateModelSerializer
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AgreementDetailModelSerializer
        return super().get_serializer_class()