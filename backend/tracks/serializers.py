from rest_framework import serializers
from tracks.models import TrackPoint


class TrackPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackPoint
        fields = ("id", "point_x", "point_y", "file_name")
