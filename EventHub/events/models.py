from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
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


class Session(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sessions',
    )

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='announcements',
    )

    def __str__(self):
        return self.title


class Text(models.Model):
    body = models.TextField()

    materials = GenericRelation(
        "EventMaterial",
        content_type_field="content_type",
        object_id_field="object_id",
    )


class File(models.Model):
    file = models.FileField(upload_to="event_files/")


class Image(models.Model):
    image = models.ImageField(upload_to="event_images/")


class Video(models.Model):
    url = models.URLField()


class EventMaterial(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="materials",
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )

    object_id = models.PositiveIntegerField()

    content = GenericForeignKey(
        "content_type",
        "object_id",
    )
