from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='events',
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_events",
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"slug": self.slug})