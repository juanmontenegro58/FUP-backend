from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.company import (
    CompanyModelSerializer,
    CompanyDetailSerializer
)
from ..models import (
    Company
)
from ..filters.company import (
    CompanyFilter
)

class CompanyViewSet(viewsets.ModelViewSet):
    
    serializer_class = CompanyModelSerializer
    queryset = Company.objects.all()
    http_method_names = ['get', 'post', 'put']
    filterset_class = CompanyFilter
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return super().get_serializer_class()