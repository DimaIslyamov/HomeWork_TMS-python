from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import (
    Announcement,
    Category,
    Event,
    EventMaterial,
    Session,
    Text,
    Video,
)


User = get_user_model()


class EventModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organizer = User.objects.create_user(
            username="organizer",
            password="testpass123",
        )
        cls.participant = User.objects.create_user(
            username="participant",
            password="testpass123",
        )
        cls.category = Category.objects.create(title="Backend")
        cls.event = Event.objects.create(
            title="Django Meetup",
            slug="django-meetup",
            description="Test event",
            category=cls.category,
            organizer=cls.organizer,
            is_published=True,
        )

    def test_category_str_returns_title(self):
        self.assertEqual(str(self.category), "Backend")

    def test_event_str_returns_title(self):
        self.assertEqual(str(self.event), "Django Meetup")

    def test_event_get_absolute_url_uses_slug(self):
        expected_url = reverse(
            "events:event_detail",
            kwargs={"slug": self.event.slug},
        )

        self.assertEqual(self.event.get_absolute_url(), expected_url)

    def test_event_foreign_key_relations(self):
        self.assertEqual(self.event.category, self.category)
        self.assertEqual(self.event.organizer, self.organizer)
        self.assertIn(self.event, self.category.events.all())
        self.assertIn(self.event, self.organizer.organized_events.all())

    def test_event_participants_many_to_many_relation(self):
        self.event.participants.add(self.participant)

        self.assertIn(self.participant, self.event.participants.all())
        self.assertIn(self.event, self.participant.participated_events.all())

    def test_event_slug_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Event.objects.create(
                title="Another Django Meetup",
                slug=self.event.slug,
                description="Duplicate slug",
                category=self.category,
                organizer=self.organizer,
                is_published=True,
            )

    def test_category_protected_when_events_exist(self):
        with self.assertRaises(ProtectedError):
            self.category.delete()

    def test_session_str_and_event_relation(self):
        session = Session.objects.create(
            title="Opening Keynote",
            description="Welcome session",
            start_time=timezone.now(),
            event=self.event,
        )

        self.assertEqual(str(session), "Opening Keynote")
        self.assertEqual(session.event, self.event)
        self.assertIn(session, self.event.sessions.all())

    def test_announcement_str_and_event_relation(self):
        announcement = Announcement.objects.create(
            title="Venue update",
            description="New room assigned",
            event=self.event,
        )

        self.assertEqual(str(announcement), "Venue update")
        self.assertEqual(announcement.event, self.event)
        self.assertIn(announcement, self.event.announcements.all())

    def test_event_material_generic_relation_to_text_content(self):
        text = Text.objects.create(body="Slides and useful links")
        material = EventMaterial.objects.create(
            event=self.event,
            content_type=ContentType.objects.get_for_model(text),
            object_id=text.pk,
        )

        self.assertEqual(material.content, text)
        self.assertIn(material, self.event.materials.all())
        self.assertIn(material, text.materials.all())

    def test_event_material_generic_relation_to_video_content(self):
        video = Video.objects.create(url="https://example.com/video")
        material = EventMaterial.objects.create(
            event=self.event,
            content_type=ContentType.objects.get_for_model(video),
            object_id=video.pk,
        )

        self.assertEqual(material.content, video)
        self.assertEqual(material.event, self.event)
