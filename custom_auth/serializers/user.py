from rest_framework import serializers

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
