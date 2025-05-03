from django.contrib.auth.models import (
    Permission
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import (
    CustomUser
)

class UserListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = [
            'password',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
            'is_active',
            'groups',
            'user_permissions',
            'role',
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.get_full_name()

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data['full_name'] = self.user.get_full_name()
        
        return data

class ValidatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class ValidatePasswordResponseSerializer(serializers.Serializer):
    common = serializers.BooleanField()
    similarity = serializers.BooleanField()

class ValidateDocumentNumberSerializer(serializers.Serializer):
    document_number = serializers.CharField()

class RegisterSerializer(ValidateDocumentNumberSerializer):
    password = serializers.CharField()

class PermissionsRoleListSerializer(serializers.Serializer):

    permissions = serializers.ListField(
        child = serializers.CharField()
    )