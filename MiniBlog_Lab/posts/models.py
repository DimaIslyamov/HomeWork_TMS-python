from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
