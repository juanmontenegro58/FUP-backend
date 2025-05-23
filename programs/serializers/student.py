from rest_framework import serializers

from ..models import (
    Student
)

class StudentCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user']
    
class StudentModelSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(read_only = True)
    program = serializers.StringRelatedField()
    class Meta:
        model = Student
        exclude = ['user']

class StudentListModelSerializer(serializers.ModelSerializer):

    program = serializers.StringRelatedField()

    class Meta:
        model = Student
        exclude = ['user']