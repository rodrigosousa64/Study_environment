from django.urls import path
from .views import VideosViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('videos', VideosViewSet, basename='videos')


urlpatterns = router.urls
