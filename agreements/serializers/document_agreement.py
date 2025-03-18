from rest_framework import serializers

from ..models import (
    DocumentAgreement,
    AgreementDocumentThrough
)

class DocumentAgreementModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentAgreement
        fields = '__all__'

class AgreementDocumentThroughModelSerializer(serializers.ModelSerializer):

    document_agreement = DocumentAgreementModelSerializer()

    class Meta:
        model = AgreementDocumentThrough
        exclude = [
            'created_at',
            'agreement',
            'updated_at',
        ]
