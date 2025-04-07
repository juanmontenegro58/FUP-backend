from rest_framework import serializers

from ..models import (
    Practice
)


class PracticeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = '__all__'