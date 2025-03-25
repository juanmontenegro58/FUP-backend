from rest_framework import serializers

from ..models import (
    Agreement,
    DocumentAgreement,
    AgreementDocumentThrough
)
from .document_agreement import (
    AgreementDocumentThroughModelSerializer
)
from companies.serializers.company import (
    CompanyModelSerializer
)
from programs.models import (
    Student
)
from ..models.choices import (
    AGREEMENT_DOCUMENT_UPDATE_STATUS_CHOICES
)
from ..enums import (
    AgreementDocumentStatusEnum
)
from programs.serializers.program import (
    ProgramModelSerializer
)

class AgreementDocumentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgreementDocumentThrough
        fields = '__all__'
        depth = 1

class AgreementCreateModelSerializer(serializers.ModelSerializer):

    documents = serializers.PrimaryKeyRelatedField(
        queryset = DocumentAgreement.objects.all(),
        many = True,
        write_only = True
    )
    status = serializers.CharField(read_only = True)
    
    class Meta:
        model = Agreement
        exclude = ['students']

    def validate(self, attrs):
        initial_date = attrs['initial_date']
        end_date = attrs['end_date']

        if initial_date > end_date:
            raise serializers.ValidationError({
                'end_date': 'La fecha de finalización debe ser posterior a la fecha inicial'
            })
        return attrs

    def validate_documents(self, value):
        """ Valida que la lista de documentos no este vacia. """
        if not value:
            raise serializers.ValidationError(
                'Debe incluir al menos un documento en el convenio'
            )
        return value

    def create(self, validated_data):
        documents = validated_data.pop('documents')

        agreement = Agreement.objects.create(**validated_data)
        agreement.documents.add(*documents)
        return agreement
    
class AgreementDetailModelSerializer(serializers.ModelSerializer):

    documents = AgreementDocumentThroughModelSerializer(
        source = 'agreementdocumentthrough_set',
        many = True, 
        read_only = True
    )
    company = CompanyModelSerializer()
    program = ProgramModelSerializer()
    
    class Meta:
        model = Agreement
        exclude = ['students']

class AgreementDocumentUploadSerializer(serializers.Serializer):

    files = serializers.ListField(
        child = serializers.FileField(),
        allow_empty = False
    )
    through_ids = serializers.ListField(
        child = serializers.IntegerField(),
        allow_empty = False
    )

    def validate(self, attrs):
        if len(attrs['files']) != len(set(attrs['through_ids'])):
            raise serializers.ValidationError(
                'La información enviada no es correcta o no tiene el formato esperado.'
            )
        return attrs
    
class AgreementAssignStudentSerializer(serializers.Serializer):

    student = serializers.PrimaryKeyRelatedField(
        queryset = Student.objects.all()
    )

class AgreementDocumentChangeStateSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices = AGREEMENT_DOCUMENT_UPDATE_STATUS_CHOICES
    )
    comment = serializers.CharField(
        allow_null = True
    )

    def validate(self, attrs):
        if attrs['status'] == AgreementDocumentStatusEnum.RECHAZADO.value and not attrs.get('comment'):
            raise serializers.ValidationError({'comment': 'Debes proporcionar un comentario.'})

        return attrs