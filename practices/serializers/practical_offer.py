from rest_framework import serializers

from ..models import (
    PracticalOffer
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