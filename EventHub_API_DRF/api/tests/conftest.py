import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient

from api.models import Category, Event


@pytest.fixture
def organizer():
    user_model = get_user_model()

    return user_model.objects.create_user(
        username="organizer",
        password="testpass123",
        role="ORGANIZER",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def attendee():
    user_model = get_user_model()

    return user_model.objects.create_user(
        username="attendee",
        password="testpass123",
        role="ATTENDEE",
    )


@pytest.fixture
def category():
    return Category.objects.create(
        name="Backend",
        slug="backend",
    )


@pytest.fixture
def second_organizer():
    user_model = get_user_model()

    return user_model.objects.create_user(
        username="second-organizer",
        password="testpass123",
        role="ORGANIZER",
    )


@pytest.fixture
def second_attendee():
    user_model = get_user_model()

    return user_model.objects.create_user(
        username="second-attendee",
        password="testpass123",
        role="ATTENDEE",
    )


@pytest.fixture
def make_event(organizer, category):
    def _make_event(**overrides):
        data = {
            "organizer": organizer,
            "category": category,
            "title": "Django Meetup",
            "slug": "django-meetup",
            "description": "Django event",
            "starts_at": timezone.now(),
            "capacity": 50,
            "is_published": True,
        }
        data.update(overrides)
        return Event.objects.create(**data)

    return _make_event


@pytest.fixture
def published_event(make_event):
    return make_event()


@pytest.fixture
def unpublished_event(make_event):
    return make_event(
        title="Draft Event",
        slug="draft-event",
        description="Unpublished event",
        is_published=False,
    )
