from django.urls import path
from .views import VideosViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register("videos", VideosViewSet, basename="videos")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = router.urls
