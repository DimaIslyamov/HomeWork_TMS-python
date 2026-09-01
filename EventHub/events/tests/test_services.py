from django.contrib.auth import get_user_model
from django.test import TestCase

from events.models import Category, Event
from events.services import (
    EventRegistrationError,
    cancel_registration,
    register_for_event,
)


User = get_user_model()


class EventRegistrationServiceTest(TestCase):
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

    def test_register_for_event_adds_participant(self):
        register_for_event(self.event, self.participant)

        self.assertTrue(
            self.event.participants.filter(pk=self.participant.pk).exists()
        )

    def test_register_for_event_rejects_organizer(self):
        with self.assertRaisesMessage(
            EventRegistrationError,
            "Organizer cannot register for own event.",
        ):
            register_for_event(self.event, self.organizer)

        self.assertFalse(
            self.event.participants.filter(pk=self.organizer.pk).exists()
        )

    def test_register_for_event_is_idempotent_for_existing_participant(self):
        register_for_event(self.event, self.participant)
        register_for_event(self.event, self.participant)

        self.assertEqual(self.event.participants.count(), 1)

    def test_cancel_registration_removes_participant(self):
        self.event.participants.add(self.participant)

        cancel_registration(self.event, self.participant)

        self.assertFalse(
            self.event.participants.filter(pk=self.participant.pk).exists()
        )

    def test_cancel_registration_is_safe_for_non_participant(self):
        cancel_registration(self.event, self.participant)

        self.assertEqual(self.event.participants.count(), 0)
