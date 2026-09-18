from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ATTENDEE = "ATTENDEE", "Attendee"
        ORGANIZER = "ORGANIZER", "Organizer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATTENDEE,
    )
    email_confirmed = models.BooleanField(default=False)
    