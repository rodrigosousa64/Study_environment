from django.urls import path
from .views import VideosViewSet, CategoryViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

# pyrefly: ignore [missing-import]
from rest_framework_nested import routers

router = DefaultRouter(trailing_slash=False)
router.register("videos", VideosViewSet, basename="videos")
router.register("category", CategoryViewSet, basename="category")

videos_router = routers.NestedDefaultRouter(router, "videos", lookup="video")
videos_router.register("comments", CommentViewSet, basename="videos-comments")

urlpatterns = router.urls + videos_router.urls
