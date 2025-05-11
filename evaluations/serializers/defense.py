from django.db import transaction
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ..models import (
    Defense,
    DefenseStudentThrough,
    DefenseTeacherThrough,
    DefenseComment,
    DocumentDefense
)
from programs.models import (
    Student
)
from programs.serializers.student import (
    StudentModelSerializer
)
from .teacher import (
    TeacherDefenseSerializer,
    TeacherModelSerializer
)
from ..enums import (
    DefenseStatusEnum
)
from ..models.choices import (
    DEFENSE_RESULT_CHOICES
)

class DocumentDefenseModelSerializer(serializers.ModelSerializer):

    uploaded_by = serializers.StringRelatedField()
    class Meta:
        model = DocumentDefense
        fields = ['name', 'file', 'uploaded_by', 'updated_at']

class DefenseStudentThroughModelSerializer(serializers.ModelSerializer):

    student = StudentModelSerializer()
    
    class Meta:
        model = DefenseStudentThrough
        exclude = ['defense']

class DefenseTeacherThroughModelSerializer(serializers.ModelSerializer):

    teacher = TeacherModelSerializer()
    
    class Meta:
        model = DefenseTeacherThrough
        exclude = ['defense']

class DefenseModelSerializer(serializers.ModelSerializer):

    students = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all(),
        many = True
    )
    teachers = TeacherDefenseSerializer(
        many = True,
        source="defenseteacherthrough_set"
    )

    class Meta:
        model = Defense
        exclude = ['status', 'result']

    def validate(self, attrs):
        application_date = attrs['application_date']
        scheduled_date = attrs['scheduled_date']
        if application_date > scheduled_date:
            raise serializers.ValidationError('La fecha de solicitud no puede ser posterior a la fecha programada')
        
        if len(attrs['students']) != len(set(attrs['students'])):
            raise serializers.ValidationError('No puedes asignar estudiantes duplicados')

        teachers = attrs['defenseteacherthrough_set']
        teachers_id = [teacher['teacher'].pk for teacher in teachers]

        if len(teachers_id) != len(set(teachers_id)):
            raise serializers.ValidationError('No puedes asignar docentes duplicados.')

        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        students = validated_data.pop('students')
        teachers = validated_data.pop('defenseteacherthrough_set')
        
        defense = Defense.objects.create(**validated_data)
        defense.students.add(*students)

        for teacher in teachers:
            DefenseTeacherThrough.objects.create(
                defense = defense,
                teacher = teacher['teacher'],
                role = teacher['role']
            )
        return defense
    
    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.status == DefenseStatusEnum.COMPLETADA.value:
            raise serializers.ValidationError({'application_date': 'No se puede modificar una sustentación completada'})
        validated_data.pop('application_date')
        validated_data.pop('scheduled_date')
        students = validated_data.pop('students')
        teachers = validated_data.pop('defenseteacherthrough_set')

        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        instance.save()

        if students is not None:
            instance.students.set(students)

        if teachers is not None:
            instance.teachers.clear()
            for teacher in teachers:
                DefenseTeacherThrough.objects.create(
                defense = instance,
                teacher = teacher['teacher'],
                role = teacher['role']
            )

        return instance
    
class DefenseListModelSerializer(serializers.ModelSerializer):

    students = serializers.SerializerMethodField(method_name = 'get_students')
    class Meta:
        model = Defense
        exclude = ['teachers']
    @extend_schema_field(
        serializers.ListField(
            child = serializers.CharField(),
            help_text = 'Lista de nombres de los estudiantes asociados'
        )
    )
    def get_students(self, obj):
        return [student.full_name for student in obj.students.all()]

class DefenseDetailModelSerializer(serializers.ModelSerializer):

    students = DefenseStudentThroughModelSerializer(
        many = True,
        source = 'defensestudentthrough_set'
    )
    teachers = DefenseTeacherThroughModelSerializer(
        many = True,
        source = 'defenseteacherthrough_set'
    )
    documentdefense_set = DocumentDefenseModelSerializer(many = True)

    class Meta:
        model = Defense
        fields = '__all__'

class DefenseCommentModelSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField()
    class Meta:
        model = DefenseComment
        exclude = ['defense']

class DefenseRescheduleSerializer(serializers.Serializer):

    comment = serializers.CharField()
    new_scheduled_date = serializers.DateField()

class DefenseCommentSerializer(serializers.Serializer):
    comment = serializers.CharField()

class DefenseFinishSerializer(serializers.Serializer):
    result = serializers.ChoiceField(
        choices = DEFENSE_RESULT_CHOICES
    )
    supporting_document = serializers.FileField(
        help_text = 'Acta de sustentación'
    )