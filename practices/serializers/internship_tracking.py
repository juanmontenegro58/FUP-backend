from rest_framework import serializers

from ..models import (
    InternshipTracking,
)


class InternshipTrackingModelSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = InternshipTracking
        exclude = ['practice']
