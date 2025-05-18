from django.contrib.auth.models import (
    Group,
    Permission
)
from rest_framework import serializers

class RoleModelSerializer(serializers.ModelSerializer):

    permissions = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Permission.objects.all(),
        allow_empty = False
    )
    
    class Meta:
        model = Group
        fields = '__all__'

class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id','name']