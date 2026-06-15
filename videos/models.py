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

    # comments = models.ManyToManyField(Comment, related_name="videos", blank=True, null=True, default=None)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(
        Videos, on_delete=models.CASCADE, related_name="comentarios"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comentarios"
    )

    def __str__(self):
        return f"Comentario de {self.author.username} em {self.created_at}"
