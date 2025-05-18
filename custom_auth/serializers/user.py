from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    Group
)
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import (
    CustomUser
)

class UserListModelSerializer(serializers.ModelSerializer):

    role = serializers.StringRelatedField()
    class Meta:
        model = CustomUser
        exclude = [
            'password',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
            'groups',
            'user_permissions',
        ]

class UserCreateModelSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.PrimaryKeyRelatedField(
        queryset = Group.objects.all()
    )
    new_password = serializers.CharField(
        write_only = True,
        required = False
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'role',
            'email',
            'new_password'
        ]

    def validate(self, attrs):
        if self.instance is None:
            if 'new_password' not in attrs:
                raise serializers.ValidationError({'new_password': 'La constraseña es obligatoria'})
        return attrs

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('new_password')
        user: CustomUser = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = None
        if 'new_password' in validated_data:
            password = validated_data.pop('new_password')
        user: CustomUser = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

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