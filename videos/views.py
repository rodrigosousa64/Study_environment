from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Videos

from .serializers import VideosSerializer


class Videos_list_views(APIView):
    def get(self, request):
        serializer = VideosSerializer(Videos.objects.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = VideosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
