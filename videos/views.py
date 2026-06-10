from rest_framework import viewsets
from .models import Videos
from .serializers import VideosSerializer
from rest_framework.permissions import IsAuthenticated




class VideosViewSet(viewsets.ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    permission_classes = [IsAuthenticated]



