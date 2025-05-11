from rest_framework import serializers

class StatsAgreementSerializer(serializers.Serializer):
    total = serializers.IntegerField(
        min_value = 0
    )
    active = serializers.IntegerField(
        min_value = 0
    )
    inactive = serializers.IntegerField(
        min_value = 0
    )
    expiring_soon = serializers.IntegerField(
        min_value = 0
    )