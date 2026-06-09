from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Videos

class VideosAPITests(APITestCase):

    def setUp(self):
        # Criando um vídeo de exemplo para ser usado nos testes
        self.video = Videos.objects.create(
            title="Test Video",
            description="Test Description",
            video_url="http://test.com/video.mp4"
        )
        self.list_url = reverse("videos_list")
        self.detail_url = reverse("videos_itens", kwargs={"id": self.video.id})

    def test_get_videos_list(self):
        """Testa a listagem de todos os vídeos"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Video")

    def test_create_video_success(self):
        """Testa a criação de um novo vídeo com dados válidos"""
        data = {
            "title": "New Video",
            "description": "New Description",
            "video_url": "http://newvideo.com/video.mp4"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Videos.objects.count(), 2)

    def test_create_video_bad_request(self):
        """Testa a criação de um vídeo com dados inválidos"""
        data = {
            "title": "New Video",
            # Faltando description e video_url
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_video_item_success(self):
        """Testa a busca de um vídeo específico"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Video")

    def test_get_video_item_not_found(self):
        """Testa a busca de um vídeo inexistente (deve retornar 404)"""
        url = reverse("videos_itens", kwargs={"id": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Video nao encontrado")

    def test_update_video_success(self):
        """Testa a atualização parcial de um vídeo"""
        data = {"title": "Updated Title"}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, "Updated Title")
        self.assertEqual(response.data["message"], "Video atualizado com sucesso")

    def test_update_video_bad_request(self):
        """Testa a atualização de um vídeo com dados inválidos"""
        data = {"title": ""} # String vazia para campo obrigatório
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_video_success(self):
        """Testa a exclusão de um vídeo"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Videos.objects.count(), 0)
        self.assertEqual(response.data["message"], "Video deletado com sucesso")

    def test_delete_video_not_found(self):
        """Testa a exclusão de um vídeo inexistente (deve retornar 404)"""
        url = reverse("videos_itens", kwargs={"id": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Video nao encontrado")
