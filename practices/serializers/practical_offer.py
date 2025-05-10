from rest_framework import serializers

from ..models import (
    PracticalOffer
)
from agreements.serializers.agreement import (
    AgreementNestedCompanySerializer
)

class PracticalOfferCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalOffer
        exclude = ['students']

class PracticalOfferListModelSerializer(serializers.ModelSerializer):

    agreement = serializers.StringRelatedField()

    class Meta:
        model = PracticalOffer
        fields = ['title', 'close_date', 'vacancies', 'agreement']

class PracticalOfferDetailSerializer(serializers.ModelSerializer):

    agreement = AgreementNestedCompanySerializer()
    class Meta:
        model = PracticalOffer
        exclude = ['students']