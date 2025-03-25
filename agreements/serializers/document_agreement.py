from rest_framework import serializers

from ..models import (
    DocumentAgreement,
    AgreementDocumentThrough,
    AgreementDocumentComment
)
from custom_auth.serializers.user import (
    UserListModelSerializer
)

class AgreementDocumentCommentModelSerializer(serializers.ModelSerializer):

    created_by = UserListModelSerializer()
    class Meta:
        model = AgreementDocumentComment
        exclude = ['agreement_document']

class DocumentAgreementModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentAgreement
        fields = '__all__'

class AgreementDocumentThroughModelSerializer(serializers.ModelSerializer):

    document_agreement = DocumentAgreementModelSerializer()
    uploaded_by = UserListModelSerializer()
    comments = AgreementDocumentCommentModelSerializer(
        many = True,
        source = 'agreementdocumentcomment_set'
    )

    class Meta:
        model = AgreementDocumentThrough
        exclude = [
            'created_at',
            'agreement',
            'updated_at',
        ]
