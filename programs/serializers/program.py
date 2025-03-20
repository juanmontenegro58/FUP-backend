from rest_framework import serializers

from ..models import (
    Program
)

class ProgramModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'