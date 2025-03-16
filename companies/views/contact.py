from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.contact import (
    ContactModelSerializer,
    ContactDetailSerializer
)
from ..models import (
    Contact
)

class ContactViewSet(viewsets.ModelViewSet):

    serializer_class = ContactModelSerializer
    queryset = Contact.objects.all()
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContactDetailSerializer
        return super().get_serializer_class()