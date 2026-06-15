from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.urls import reverse
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import Videos, Category, Comment
from .serializers import VideosSerializer
from .validators import no_bad_words
from .permissions import Is_author_or_readonly

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(nome="Tech", slug="tech")
        self.video = Videos.objects.create(
            title="12345 Test Video",
            description="Test Description",
            video_url="http://test.com/video.mp4",
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            comment="Great video!",
            video=self.video,
            author=self.user
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Tech")

    def test_videos_str(self):
        self.assertEqual(str(self.video), "12345 Test Video")

    def test_comment_str(self):
        expected_str = f"Comentario de {self.user.username} em {self.comment.created_at}"
        self.assertEqual(str(self.comment), expected_str)


class ValidatorTests(TestCase):
    def test_no_bad_words_success(self):
        self.assertEqual(no_bad_words("laranja"), "laranja")
        self.assertEqual(no_bad_words("good content"), "good content")

    def test_no_bad_words_failure(self):
        with self.assertRaises(DRFValidationError):
            no_bad_words("this is an apple")
        with self.assertRaises(DRFValidationError):
            no_bad_words("banana is here")


class SerializerTests(TestCase):
    def test_validate_title_length(self):
        serializer = VideosSerializer()
        with self.assertRaisesMessage(DRFValidationError, "Title must be at least 5 characters long"):
            serializer.validate_title("1234")

    def test_validate_title_starts_with_number(self):
        serializer = VideosSerializer()
        with self.assertRaisesMessage(DRFValidationError, "Title must start with a number"):
            serializer.validate_title("Invalid Title")

    def test_validate_title_success(self):
        serializer = VideosSerializer()
        valid_title = "1234567890 Valid"
        self.assertEqual(serializer.validate_title(valid_title), valid_title)


class PermissionTests(TestCase):
    def setUp(self):
        self.user_author = User.objects.create_user(username="author", password="password")
        self.user_other = User.objects.create_user(username="other", password="password")
        self.video = Videos.objects.create(
            title="1234567890 Test",
            description="Desc",
            video_url="http://test.com/vid.mp4",
            author=self.user_author
        )
        self.permission = Is_author_or_readonly()
        self.factory = APIRequestFactory()

    def test_safe_method_allowed(self):
        request = self.factory.get('/')
        request.user = self.user_other
        self.assertTrue(self.permission.has_object_permission(request, None, self.video))

    def test_unsafe_method_author_allowed(self):
        request = self.factory.put('/')
        request.user = self.user_author
        self.assertTrue(self.permission.has_object_permission(request, None, self.video))

    def test_unsafe_method_other_denied(self):
        request = self.factory.put('/')
        request.user = self.user_other
        self.assertFalse(self.permission.has_object_permission(request, None, self.video))


class CategoryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.category = Category.objects.create(nome="Tech", slug="tech")
        self.list_url = reverse("category-list")
        self.detail_url = reverse("category-detail", kwargs={"pk": self.category.id})

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_category_unauthenticated(self):
        data = {"nome": "Science", "slug": "science"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {"nome": "Science", "slug": "science"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class VideosAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.category = Category.objects.create(nome="Tech", slug="tech")
        self.video = Videos.objects.create(
            title="1234567890 Test",
            description="Test Desc",
            video_url="http://test.com/vid.mp4",
            author=self.user,
            category=self.category
        )
        self.list_url = reverse("videos-list")
        self.detail_url = reverse("videos-detail", kwargs={"pk": self.video.id})

    def test_list_videos(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_video_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "1234567890 New Video",
            "description": "Desc",
            "video_url": "http://new.com/vid.mp4",
            "category": self.category.slug
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Videos.objects.count(), 2)
        new_video = Videos.objects.get(title="1234567890 New Video")
        self.assertEqual(new_video.author, self.user)

    def test_create_video_bad_words(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "1234567890 banana Video",
            "description": "Desc",
            "video_url": "http://new.com/vid.mp4"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_update_video_author(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "1234567890 Updated"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.video.refresh_from_db()
        self.assertEqual(self.video.title, "1234567890 Updated")

    def test_update_video_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"title": "1234567890 Updated"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_video_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_video_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(username="other", password="password")
        self.video = Videos.objects.create(
            title="1234567890 Test",
            description="Test Desc",
            video_url="http://test.com/vid.mp4",
            author=self.user
        )
        self.comment = Comment.objects.create(
            comment="First comment",
            video=self.video,
            author=self.user
        )
        self.list_url = reverse("videos-comments-list", kwargs={"video_pk": self.video.id})
        self.detail_url = reverse("videos-comments-detail", kwargs={"video_pk": self.video.id, "pk": self.comment.id})

    def test_list_comments(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"comment": "New comment!"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        new_comment = Comment.objects.last()
        self.assertEqual(new_comment.author, self.other_user)
        self.assertEqual(new_comment.video, self.video)

    def test_update_comment_author(self):
        self.client.force_authenticate(user=self.user)
        data = {"comment": "Updated comment"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        data = {"comment": "Updated comment"}
        response = self.client.patch(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
