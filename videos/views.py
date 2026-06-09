from core import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Videos
from django.shortcuts import get_object_or_404
from django.http import Http404


from .serializers import VideosSerializer


class Videos_list_views(APIView):
    def get(self, request):
        serializer = VideosSerializer(Videos.objects.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        try:
            serializer = VideosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"message": "Video nao encontrado"}, status.HTTP_404_NOT_FOUND
            )


class Videos_item_views(APIView):
    def get(self, request, id):
        try:
            video = get_object_or_404(Videos, id=id)
            serializer = VideosSerializer(video)
            return Response(serializer.data, status.HTTP_200_OK)
        except Http404:
            return Response(
                {"message": "Video nao encontrado"}, status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):
        video = get_object_or_404(Videos, id=id)
        serializer = VideosSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Video atualizado com sucesso", "telemetry": serializer.data},
                status.HTTP_200_OK,
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            video = get_object_or_404(Videos, id=id)
            video.delete()
            
            return Response(
                {"message":"Video deletado com sucesso"}, status.HTTP_200_OK
            )
        except Http404:
            return Response(
                {"message": "Video nao encontrado"}, status.HTTP_404_NOT_FOUND
            )
