from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from rest_framework.test import APIClient

from api.models import Category, Event, Session


User = get_user_model()


class EventQueryCountTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.organizer = User.objects.create_user(
            username="organizer_test",
            password="testpass123",
            role="ORGANIZER",
        )

        # organizer = User.objects.create_user(
        #     username="organizer_test",
        #     password="testpass123",
        #     role="ORGANIZER",
        # )

        category = Category.objects.create(
            name="Backend",
            slug="backend",
        )

        self.attendee = User.objects.create_user(
            username="attendee_test",
            password="testpass123",
            role="ATTENDEE",
        )

        for event_number in range(1, 4):
            event = Event.objects.create(
                organizer=self.organizer,
                category=category,
                title=f"Event {event_number}",
                slug=f"event-{event_number}",
                description="Test event",
                starts_at=timezone.now() + timedelta(days=event_number),
                capacity=100,
                is_published=True,
            )

            for session_number in range(1, 3):
                Session.objects.create(
                    event=event,
                    title=f"Session {session_number}",
                    description="Test session",
                    starts_at=event.starts_at,
                )

    def test_event_patch_queries(self):
        event = Event.objects.first()

        self.client.force_authenticate(user=self.organizer)

        with CaptureQueriesContext(connection) as queries:
            response = self.client.patch(
                f"/api/events/{event.pk}/",
                {"title": "Updated Event"},
                format="json",
            )

        print("\nSTATUS:", response.status_code)
        print("TOTAL QUERIES:", len(queries))

        for number, query in enumerate(queries.captured_queries, start=1):
            print(f"\nQUERY {number}:")
            print(query["sql"])

    def test_event_list_queries(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get("/api/events/?page_size=10")

        print("\nSTATUS:", response.status_code)
        print("EVENTS:", len(response.data["results"]))
        print("TOTAL QUERIES:", len(queries))

        for number, query in enumerate(queries.captured_queries, start=1):
            print(f"\nQUERY {number}:")
            print(query["sql"])

    def test_event_retrieve_queries(self):
        event = Event.objects.first()

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(f"/api/events/{event.pk}/")

        print("\nSTATUS:", response.status_code)
        print("EVENT:", response.data["title"])
        print("SESSIONS:", len(response.data["sessions"]))
        print("TOTAL QUERIES:", len(queries))

        for number, query in enumerate(queries.captured_queries, start=1):
            print(f"\nQUERY {number}:")
            print(query["sql"])

    def test_register_queries(self):
        event = Event.objects.first()

        self.client.force_authenticate(user=self.attendee)

        with CaptureQueriesContext(connection) as queries:
            response = self.client.post(
                f"/api/events/{event.pk}/register/"
            )

        print("\nSTATUS:", response.status_code)
        print("TOTAL QUERIES:", len(queries))

        for number, query in enumerate(queries.captured_queries, start=1):
            print(f"\nQUERY {number}:")
            print(query["sql"])