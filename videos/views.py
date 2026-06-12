from rest_framework import viewsets
from .models import Videos, Category
from .serializers import VideosSerializer, Category_serializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import Is_author_or_readonly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_serializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VideosViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, Is_author_or_readonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)