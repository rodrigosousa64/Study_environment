from rest_framework.response import Response
from rest_framework import generics
from .models import Videos
from .serializers import VideosSerializer

class Videos_list_views(generics.ListCreateAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer

class Videos_item_views(generics.RetrieveUpdateDestroyAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer


