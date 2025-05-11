from rest_framework import serializers

class DashboardReportSerializer(serializers.Serializer):

    labels = serializers.ListField(
        child = serializers.CharField()
    )
    series = serializers.ListField(
        child = serializers.IntegerField()
    )