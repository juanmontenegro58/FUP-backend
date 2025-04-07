from rest_framework import serializers

from ..models import (
    Practice
)
from programs.serializers.student import (
    StudentModelSerializer
)
from evaluations.serializers.teacher import (
    TeacherModelSerializer
)

class PracticeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        exclude = ['status']

class PracticeListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = '__all__'

class PracticeDetailModelSerializer(serializers.ModelSerializer):

    student = StudentModelSerializer()
    teacher = TeacherModelSerializer()

    class Meta:
        model = Practice
        fields = '__all__'