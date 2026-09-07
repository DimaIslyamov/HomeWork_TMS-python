from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="events",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    starts_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['starts_at']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(capacity__gt=0),
                name="event_capacity_gte_0",
            ),
        ]

    def __str__(self):
        return self.title
