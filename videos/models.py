from django.contrib.auth import models
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categories"


class Videos(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="videos",
    )

    def __str__(self):
        return self.title
