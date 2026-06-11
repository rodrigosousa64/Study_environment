from rest_framework import viewsets
from .models import Videos
from .serializers import VideosSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import Is_author_or_readonly




class VideosViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,Is_author_or_readonly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



