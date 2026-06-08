from django.urls import path
from .views import Videos_list_views

urlpatterns = [
    path("videos", Videos_list_views.as_view(), name="videos_list"),
]
