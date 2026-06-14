from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from .models import Videos, Category, Comment
from .serializers import VideosSerializer, Category_serializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import Is_author_or_readonly
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import Videos_pagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_serializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class VideosViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, Is_author_or_readonly]
    filterset_fields = ["category__slug", "author__username"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]   
    ordering = ["-created_at"]
    pagination_class = Videos_pagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, Is_author_or_readonly]

    def get_queryset(self):
        return Comment.objects.filter(video=self.kwargs["video_pk"])

    def perform_create(self, serializer):
        video = get_object_or_404(Videos, pk=self.kwargs["video_pk"])
        serializer.save(author=self.request.user, video=video)
