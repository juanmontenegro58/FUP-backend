from rest_framework import serializers

from ..models import (
    Teacher
)
from ..models.choices import (
    DEFENSE_TEACHER_ROLE_CHOICES
)

class TeacherModelSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        read_only = True
    )
    
    class Meta:
        model = Teacher
        exclude = ['user']

class TeacherDefenseSerializer(serializers.Serializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset = Teacher.objects.all()
    )
    role = serializers.ChoiceField(
        choices = DEFENSE_TEACHER_ROLE_CHOICES
    )