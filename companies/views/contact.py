from django.core.exceptions import (
    PermissionDenied
)
from rest_framework import viewsets
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema
)

from ..serializers.contact import (
    ContactModelSerializer,
    ContactDetailSerializer
)
from ..models import (
    Contact
)
from core.constants.text import (
    NOT_PERMISSION
)

@extend_schema_view(
    list=extend_schema(
        summary="Listar contactos",
        description="Devuelve una lista de todos los contactos registrados.",
        tags = ['Contacto']
    ),
    retrieve=extend_schema(
        summary="Obtener un contacto",
        description="Obtiene los detalles de un contacto específico por su ID.",
        tags = ['Contacto']
    ),
    create=extend_schema(
        summary="Crear un nuevo contacto",
        description="Registra un nuevo contacto en el sistema.",
        tags = ['Contacto']
    ),
    update=extend_schema(
        summary="Actualizar un contacto",
        description="Actualiza todos los campos de un contacto existente.",
        tags = ['Contacto']
    ),
    
)
class ContactViewSet(viewsets.ModelViewSet):

    serializer_class = ContactModelSerializer
    queryset = Contact.objects.all()
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContactDetailSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        action_permissions = {
            'list': 'companies.view_contact',
            'retrieve': 'companies.view_contact',
            'create': 'companies.add_contact',
            'update': 'companies.change_contact',
        }
        perm = action_permissions.get(self.action)
        if perm and not self.request.user.has_perm(perm):
            raise PermissionDenied(NOT_PERMISSION)
        return super().get_permissions()