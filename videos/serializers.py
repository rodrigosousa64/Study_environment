from rest_framework import serializers
from .models import Videos, Category, Comment
from .validators import no_bad_words


class Category_serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "nome", "slug"]


class VideosSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[no_bad_words])

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

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )
        if not value[0].isdigit():
            raise serializers.ValidationError("Title must start with a number")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "comment", "created_at", "video", "author", "author_name"]
        read_only_fields = ["id", "created_at", "video", "author"]
