from rest_framework import serializers
from django.core.exceptions import (
    ValidationError
)

from ..models import (
    Agreement,
    DocumentAgreement,
    AgreementDocumentThrough,
    Favoritos
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
from core.validators.validator import (
    ValidatorRules
)
from ..validators.agreement import (
    AgreementMinSixMonthsValidator
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
        validator = ValidatorRules()
        validator.add_rules(rules = [AgreementMinSixMonthsValidator])
        try:
            validator.validate(attrs)
        except ValidationError as e:
            raise serializers.ValidationError({
                'end_date': e.message
            })
        return attrs

    def validate_documents(self, value):
        """ Valida que la lista de documentos no este vacia. """
        if not value:
            raise serializers.ValidationError(
                'Debe incluir al menos un documento en el convenio'
            )
        return value
class AgreementDetailModelSerializer(serializers.ModelSerializer):

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
    
class AgreementNestedSerializer(serializers.ModelSerializer):

    company = CompanyModelSerializer()

    class Meta:
        model = Agreement
        exclude = ['documents', 'program', 'students']

class AgreementNestedCompanySerializer(serializers.ModelSerializer):

    company = CompanyModelSerializer()

    class Meta:
        model = Agreement
        fields = [
            'id',
            'company',
            'name',
            'initial_date',
            'end_date',
            'description'
        ]

class FavoritosModelSerializer(serializers.ModelSerializer):

    agreement = AgreementNestedCompanySerializer()
    class Meta:
        model = Favoritos
        fields = '__all__'

class FavoritosCreateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favoritos
        fields = '__all__'