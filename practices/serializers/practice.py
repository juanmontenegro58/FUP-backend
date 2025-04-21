from rest_framework import serializers


from ..models import (
    Practice,
    DocumentPractice
)
from programs.serializers.student import (
    StudentModelSerializer
)
from evaluations.serializers.teacher import (
    TeacherModelSerializer
)
from agreements.serializers.agreement import (
    AgreementNestedSerializer
)

class DocumentPracticeModelSerializer(serializers.ModelSerializer):

    uploaded_by = serializers.StringRelatedField()
    class Meta:
        model = DocumentPractice
        exclude = ['practice']

class PracticeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        exclude = ['status', 'program']

    def create(self, validated_data):
        program = validated_data['student'].program
        practice = Practice.objects.create(
            **validated_data,
            program = program
        )
        return practice

class PracticeListModelSerializer(serializers.ModelSerializer):

    student = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    program = serializers.StringRelatedField()
    agreement = serializers.StringRelatedField()

    class Meta:
        model = Practice
        fields = '__all__'

class PracticeDetailModelSerializer(serializers.ModelSerializer):

    student = StudentModelSerializer()
    teacher = TeacherModelSerializer()
    documents = DocumentPracticeModelSerializer(
        many = True, 
        source = 'documentpractice_set'
    )
    program = serializers.StringRelatedField()
    agreement = AgreementNestedSerializer()

    class Meta:
        model = Practice
        fields = '__all__'

class PracticeDocumentCreateSerializer(serializers.Serializer):
    names = serializers.ListField(
        child = serializers.CharField(),
        allow_empty = False
    )
    files = serializers.ListField(
        child = serializers.FileField(),
        allow_empty = False
    )

    def validate(self, attrs):
        if len(attrs['names']) != len(attrs['files']):
            raise serializers.ValidationError("Información no válida")
        return attrs