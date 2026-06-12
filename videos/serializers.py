from rest_framework import serializers
from .models import Videos, Category


class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "nome", "slug"]


class VideosSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        allow_null=True,
        required=False,
    )
    category_info = Category_serializer(source="category", read_only=True)

    class Meta:
        model = Videos
        fields = [
            "id",
            "title",
            "author",
            "description",
            "video_url",
            "created_at",
            "category",
            "category_info",
        ]
        read_only_fields = ["id", "created_at", "author", "category_info", "category"]
