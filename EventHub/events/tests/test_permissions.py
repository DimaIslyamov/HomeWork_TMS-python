from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from events.models import Announcement, Category, Event


User = get_user_model()


class EventPermissionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="owner",
            password="testpass123",
        )
        cls.other_user = User.objects.create_user(
            username="other",
            password="testpass123",
        )
        cls.participant = User.objects.create_user(
            username="participant",
            password="testpass123",
        )
        cls.category = Category.objects.create(title="Backend")
        cls.event = Event.objects.create(
            title="Owner Event",
            slug="owner-event",
            description="Owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=True,
        )
        cls.draft_event = Event.objects.create(
            title="Draft Event",
            slug="draft-event",
            description="Not public",
            category=cls.category,
            organizer=cls.owner,
            is_published=False,
        )
        cls.announcement = Announcement.objects.create(
            title="Schedule update",
            description="The opening session starts earlier.",
            event=cls.event,
        )

    def test_anonymous_user_is_redirected_from_event_update(self):
        response = self.client.get(
            reverse("events:event_update", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_owner_can_access_event_update(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("events:event_update", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_authenticated_non_owner_cannot_access_event_update(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("events:event_update", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_is_redirected_from_announcement_update(self):
        response = self.client.get(
            reverse(
                "events:announcements_update",
                kwargs={"pk": self.announcement.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_owner_can_access_announcement_update(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse(
                "events:announcements_update",
                kwargs={"pk": self.announcement.pk},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_authenticated_non_owner_cannot_access_announcement_update(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                "events:announcements_update",
                kwargs={"pk": self.announcement.pk},
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_join_event_requires_authentication(self):
        response = self.client.post(
            reverse("events:event_join", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_non_owner_can_join_published_event(self):
        self.client.force_login(self.participant)

        response = self.client.post(
            reverse("events:event_join", kwargs={"pk": self.event.pk})
        )

        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertTrue(
            self.event.participants.filter(pk=self.participant.pk).exists()
        )

    def test_authenticated_owner_cannot_join_own_event(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("events:event_join", kwargs={"pk": self.event.pk})
        )

        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertFalse(
            self.event.participants.filter(pk=self.owner.pk).exists()
        )

    def test_authenticated_user_cannot_join_draft_event_by_direct_url(self):
        self.client.force_login(self.participant)

        response = self.client.post(
            reverse("events:event_join", kwargs={"pk": self.draft_event.pk})
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            self.draft_event.participants.filter(
                pk=self.participant.pk
            ).exists()
        )

    def test_leave_event_requires_authentication(self):
        response = self.client.post(
            reverse("events:event_leave", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_participant_can_leave_published_event(self):
        self.event.participants.add(self.participant)
        self.client.force_login(self.participant)

        response = self.client.post(
            reverse("events:event_leave", kwargs={"pk": self.event.pk})
        )

        self.assertRedirects(response, self.event.get_absolute_url())
        self.assertFalse(
            self.event.participants.filter(pk=self.participant.pk).exists()
        )
