from django.contrib.auth import get_user_model
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
)


User = get_user_model()


class PublicEventViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organizer = User.objects.create_user(
            username="organizer",
            password="testpass123",
        )
        cls.category = Category.objects.create(title="Backend")
        cls.other_category = Category.objects.create(title="Frontend")
        cls.published_event = Event.objects.create(
            title="Django Meetup",
            slug="django-meetup",
            description="Deep dive into Django",
            category=cls.category,
            organizer=cls.organizer,
            is_published=True,
        )
        cls.draft_event = Event.objects.create(
            title="Draft Event",
            slug="draft-event",
            description="Not public",
            category=cls.category,
            organizer=cls.organizer,
            is_published=False,
        )

    def test_event_list_shows_published_events_only(self):
        response = self.client.get(reverse("events:event_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_event.title)
        self.assertNotContains(response, self.draft_event.title)

    def test_event_detail_shows_published_event(self):
        response = self.client.get(self.published_event.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_event.title)

    def test_event_detail_returns_404_for_draft_event(self):
        response = self.client.get(self.draft_event.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_event_list_search_filters_by_title_and_description(self):
        Event.objects.create(
            title="Python Workshop",
            slug="python-workshop",
            description="Asyncio patterns",
            category=self.category,
            organizer=self.organizer,
            is_published=True,
        )

        response = self.client.get(
            reverse("events:event_list"),
            {"q": "django"},
        )

        self.assertContains(response, "Django Meetup")
        self.assertNotContains(response, "Python Workshop")

    def test_event_list_can_filter_by_category_url(self):
        frontend_event = Event.objects.create(
            title="CSS Conf",
            slug="css-conf",
            description="Layout and design systems",
            category=self.other_category,
            organizer=self.organizer,
            is_published=True,
        )

        response = self.client.get(
            reverse(
                "events:events_by_category",
                kwargs={"category_id": self.other_category.pk},
            )
        )

        self.assertContains(response, frontend_event.title)
        self.assertNotContains(response, self.published_event.title)

    def test_event_list_paginates_by_five_events(self):
        for index in range(6):
            Event.objects.create(
                title=f"Published Event {index}",
                slug=f"published-event-{index}",
                description="Pagination event",
                category=self.category,
                organizer=self.organizer,
                is_published=True,
            )

        response = self.client.get(reverse("events:event_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["events"]), 5)


class OrganizerEventViewsTest(TestCase):
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
        cls.category = Category.objects.create(title="Backend")
        cls.owner_event = Event.objects.create(
            title="Owner Event",
            slug="owner-event",
            description="Owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=True,
        )
        cls.draft_event = Event.objects.create(
            title="Owner Draft",
            slug="owner-draft",
            description="Draft owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=False,
        )
        cls.other_event = Event.objects.create(
            title="Other Event",
            slug="other-event",
            description="Owned by other user",
            category=cls.category,
            organizer=cls.other_user,
            is_published=True,
        )

    def test_my_event_list_requires_login(self):
        response = self.client.get(reverse("events:my_event_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_my_event_list_shows_only_current_user_events(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("events:my_event_list"))

        self.assertContains(response, self.owner_event.title)
        self.assertContains(response, self.draft_event.title)
        self.assertNotContains(response, self.other_event.title)

    def test_my_event_list_filters_by_status(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("events:my_event_list"),
            {"status": "draft"},
        )

        self.assertContains(response, self.draft_event.title)
        self.assertNotContains(response, self.owner_event.title)

    def test_my_event_list_searches_owner_events(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("events:my_event_list"),
            {"q": "Draft"},
        )

        self.assertContains(response, self.draft_event.title)
        self.assertNotContains(response, self.owner_event.title)
        self.assertNotContains(response, self.other_event.title)

    def test_event_create_requires_login(self):
        response = self.client.get(reverse("events:event_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_authenticated_user_can_create_event_as_organizer(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("events:event_create"),
            data={
                "title": "New Owner Event",
                "slug": "new-owner-event",
                "description": "Created through the form",
                "category": self.category.pk,
                "is_published": True,
            },
        )

        event = Event.objects.get(slug="new-owner-event")
        self.assertRedirects(response, event.get_absolute_url())
        self.assertEqual(event.organizer, self.owner)

    def test_owner_can_update_own_event(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "events:event_update",
                kwargs={"pk": self.owner_event.pk},
            ),
            data={
                "title": "Updated Owner Event",
                "slug": self.owner_event.slug,
                "description": "Updated description",
                "category": self.category.pk,
                "is_published": True,
            },
        )

        self.assertRedirects(response, self.owner_event.get_absolute_url())
        self.owner_event.refresh_from_db()
        self.assertEqual(self.owner_event.title, "Updated Owner Event")

    def test_other_user_cannot_update_foreign_event_by_direct_url(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:event_update",
                kwargs={"pk": self.owner_event.pk},
            ),
            data={
                "title": "Hijacked Event",
                "slug": self.owner_event.slug,
                "description": "Should not be saved",
                "category": self.category.pk,
                "is_published": True,
            },
        )

        self.assertEqual(response.status_code, 403)
        self.owner_event.refresh_from_db()
        self.assertEqual(self.owner_event.title, "Owner Event")

    def test_owner_can_delete_own_event(self):
        event = Event.objects.create(
            title="Disposable Event",
            slug="disposable-event",
            description="Will be deleted",
            category=self.category,
            organizer=self.owner,
            is_published=True,
        )
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("events:event_delete", kwargs={"pk": event.pk})
        )

        self.assertRedirects(response, reverse("events:event_list"))
        self.assertFalse(Event.objects.filter(pk=event.pk).exists())

    def test_other_user_cannot_delete_foreign_event_by_direct_url(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:event_delete",
                kwargs={"pk": self.owner_event.pk},
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Event.objects.filter(pk=self.owner_event.pk).exists())


class EventMaterialCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="material-owner",
            password="testpass123",
        )
        cls.other_user = User.objects.create_user(
            username="material-other",
            password="testpass123",
        )
        cls.category = Category.objects.create(title="Backend")
        cls.event = Event.objects.create(
            title="Owner Material Event",
            slug="owner-material-event",
            description="Owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=True,
        )

    def test_material_create_requires_login_on_get(self):
        response = self.client.get(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "text",
                },
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_owner_can_open_text_material_form(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "text",
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add Text Material")

    def test_non_owner_cannot_open_foreign_event_material_form(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "text",
                },
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_can_create_text_material(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "text",
                },
            ),
            data={
                "body": "Slides and useful links",
            },
        )

        self.assertRedirects(response, reverse("events:my_event_list"))
        text = Text.objects.get(body="Slides and useful links")
        material = EventMaterial.objects.get(event=self.event)
        self.assertEqual(material.content, text)

    def test_unknown_material_content_type_returns_404(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "unknown",
                },
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_non_owner_cannot_post_text_material_to_foreign_event(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:event_material_add",
                kwargs={
                    "pk": self.event.pk,
                    "content_type": "text",
                },
            ),
            data={
                "body": "Unauthorized material",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Text.objects.filter(body="Unauthorized material").exists())
        self.assertEqual(EventMaterial.objects.count(), 0)


class EventSessionManageViewTest(TestCase):
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
        cls.category = Category.objects.create(title="Backend")
        cls.event = Event.objects.create(
            title="Owner Event",
            slug="owner-event",
            description="Owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=True,
        )

    def test_session_manage_requires_login(self):
        response = self.client.get(
            reverse("events:event_sessions", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_owner_can_view_session_manage_page(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("events:event_sessions", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage Sessions")

    def test_other_user_gets_404_for_foreign_session_manage_page(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("events:event_sessions", kwargs={"pk": self.event.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_can_create_session_from_formset(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("events:event_sessions", kwargs={"pk": self.event.pk}),
            data={
                "sessions-TOTAL_FORMS": "1",
                "sessions-INITIAL_FORMS": "0",
                "sessions-MIN_NUM_FORMS": "0",
                "sessions-MAX_NUM_FORMS": "1000",
                "sessions-0-title": "Opening Keynote",
                "sessions-0-description": "Welcome session",
                "sessions-0-start_time": timezone.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            },
        )

        self.assertRedirects(response, reverse("events:my_event_list"))
        self.assertTrue(
            Session.objects.filter(
                event=self.event,
                title="Opening Keynote",
            ).exists()
        )


class AnnouncementViewsTest(TestCase):
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
        cls.category = Category.objects.create(title="Backend")
        cls.owner_event = Event.objects.create(
            title="Owner Event",
            slug="owner-event",
            description="Owned by owner",
            category=cls.category,
            organizer=cls.owner,
            is_published=True,
        )
        cls.other_event = Event.objects.create(
            title="Other Event",
            slug="other-event",
            description="Owned by other user",
            category=cls.category,
            organizer=cls.other_user,
            is_published=True,
        )
        cls.announcement = Announcement.objects.create(
            title="Schedule update",
            description="The opening session starts earlier.",
            event=cls.owner_event,
        )
        cls.other_announcement = Announcement.objects.create(
            title="Other announcement",
            description="Private to other organizer.",
            event=cls.other_event,
        )

    def test_announcements_list_requires_login(self):
        response = self.client.get(
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_owner_can_list_own_event_announcements(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.announcement.title)
        self.assertNotContains(response, self.other_announcement.title)

    def test_other_user_gets_404_for_foreign_event_announcements_list(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_owner_can_create_announcement_for_own_event(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "events:announcements_create",
                kwargs={"event_id": self.owner_event.pk},
            ),
            data={
                "title": "New announcement",
                "description": "Doors open at 9.",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            ),
        )
        self.assertTrue(
            Announcement.objects.filter(
                event=self.owner_event,
                title="New announcement",
            ).exists()
        )

    def test_other_user_cannot_create_announcement_for_foreign_event(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:announcements_create",
                kwargs={"event_id": self.owner_event.pk},
            ),
            data={
                "title": "Unauthorized announcement",
                "description": "Should not be saved.",
            },
        )

        self.assertEqual(response.status_code, 404)
        self.assertFalse(
            Announcement.objects.filter(
                event=self.owner_event,
                title="Unauthorized announcement",
            ).exists()
        )

    def test_owner_can_update_own_announcement(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "events:announcements_update",
                kwargs={"pk": self.announcement.pk},
            ),
            data={
                "title": "Updated schedule",
                "description": "The opening session starts later.",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            ),
        )
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, "Updated schedule")

    def test_other_user_cannot_update_foreign_announcement_by_direct_url(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:announcements_update",
                kwargs={"pk": self.announcement.pk},
            ),
            data={
                "title": "Hijacked announcement",
                "description": "Should not be saved.",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.announcement.refresh_from_db()
        self.assertEqual(self.announcement.title, "Schedule update")

    def test_owner_can_delete_own_announcement(self):
        announcement = Announcement.objects.create(
            title="Temporary announcement",
            description="Will be deleted.",
            event=self.owner_event,
        )
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse(
                "events:announcements_delete",
                kwargs={"pk": announcement.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "events:announcements_list",
                kwargs={"event_id": self.owner_event.pk},
            ),
        )
        self.assertFalse(
            Announcement.objects.filter(pk=announcement.pk).exists()
        )

    def test_other_user_cannot_delete_foreign_announcement_by_direct_url(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse(
                "events:announcements_delete",
                kwargs={"pk": self.announcement.pk},
            )
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Announcement.objects.filter(pk=self.announcement.pk).exists()
        )
