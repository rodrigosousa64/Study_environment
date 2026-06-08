from rest_framework import serializers
from .models import Videos


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = ["id", "title", "description", "video_url", "created_at"]
        read_only_fields = ["id", "created_at"]
