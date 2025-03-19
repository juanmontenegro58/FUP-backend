from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ..models import (
    Company
)
from .contact import (
    ContactModelSerializer
)

class CompanyModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

class CompanyDetailSerializer(serializers.ModelSerializer):

    contacts = serializers.SerializerMethodField(
        method_name = 'get_contacts'
    )

    class Meta:
        model = Company
        fields = '__all__'

    @extend_schema_field(ContactModelSerializer(many = True))
    def get_contacts(self, obj):
        return ContactModelSerializer(obj.contact_set.all(), many = True).data