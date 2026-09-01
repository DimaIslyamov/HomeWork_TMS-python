from django.contrib.auth import get_user_model
from django.test import TestCase

from events.forms import AnnouncementForm, EventForm
from events.models import Category, Event


User = get_user_model()


class EventFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organizer = User.objects.create_user(
            username="organizer",
            password="testpass123",
        )
        cls.category = Category.objects.create(title="Backend")
        cls.event = Event.objects.create(
            title="Existing Event",
            slug="existing-event",
            description="Existing description",
            category=cls.category,
            organizer=cls.organizer,
            is_published=True,
        )

    def test_event_form_accepts_valid_data(self):
        form = EventForm(
            data={
                "title": "New Event",
                "slug": "new-event",
                "description": "A useful event",
                "category": self.category.pk,
                "is_published": True,
            }
        )

        self.assertTrue(form.is_valid())

    def test_event_form_rejects_blank_slug_after_strip(self):
        form = EventForm(
            data={
                "title": "New Event",
                "slug": "   ",
                "description": "A useful event",
                "category": self.category.pk,
                "is_published": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["slug"])

    def test_event_form_rejects_duplicate_slug(self):
        form = EventForm(
            data={
                "title": "New Event",
                "slug": self.event.slug,
                "description": "A useful event",
                "category": self.category.pk,
                "is_published": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "Event with this slug already exists.",
            form.errors["slug"],
        )

    def test_event_form_allows_instance_to_keep_own_slug(self):
        form = EventForm(
            instance=self.event,
            data={
                "title": "Existing Event Updated",
                "slug": self.event.slug,
                "description": "Updated description",
                "category": self.category.pk,
                "is_published": False,
            },
        )

        self.assertTrue(form.is_valid())

    def test_event_form_trims_slug(self):
        form = EventForm(
            data={
                "title": "New Event",
                "slug": "  trimmed-slug  ",
                "description": "A useful event",
                "category": self.category.pk,
                "is_published": True,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["slug"], "trimmed-slug")


class AnnouncementFormTest(TestCase):
    def test_announcement_form_accepts_valid_data(self):
        form = AnnouncementForm(
            data={
                "title": "Schedule update",
                "description": "The opening session starts earlier.",
            }
        )

        self.assertTrue(form.is_valid())

    def test_announcement_form_requires_title(self):
        form = AnnouncementForm(
            data={
                "title": "",
                "description": "The opening session starts earlier.",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
