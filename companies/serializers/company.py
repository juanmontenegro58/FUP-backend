from rest_framework import serializers

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

    def get_contacts(self, obj):
        return ContactModelSerializer(obj.contact_set.all(), many = True).data