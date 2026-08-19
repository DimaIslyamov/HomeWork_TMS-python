from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


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
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2

            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}--{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"slug": self.slug})
