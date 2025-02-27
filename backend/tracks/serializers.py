from rest_framework import serializers
from .models import TrackPoint

class TrackPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPoint
        fields = "__all__"