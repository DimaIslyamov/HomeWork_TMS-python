import pytest

from django.utils import timezone

from api.models import Event, Registration

from rest_framework import status


pytestmark = pytest.mark.django_db


def assert_error_contract(response, code):
    assert set(response.data) == {"error"}
    assert set(response.data["error"]) == {"code", "message", "details"}
    assert response.data["error"]["code"] == code


def event_payload(category, **overrides):
    data = {
        "title": "DRF Meetup",
        "slug": "drf-meetup",
        "description": "DRF event",
        "starts_at": timezone.now(),
        "capacity": 50,
        "is_published": True,
        "category": category.id,
    }
    data.update(overrides)
    return data


def result_ids(response):
    return [item["id"] for item in response.data["results"]]


def test_guest_sees_only_published_events(api_client, published_event, unpublished_event):
    response = api_client.get("/api/events/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert result_ids(response) == [published_event.id]


def test_attendee_sees_only_published_events(
    api_client,
    attendee,
    published_event,
    unpublished_event,
):
    api_client.force_authenticate(user=attendee)

    response = api_client.get("/api/events/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert result_ids(response) == [published_event.id]


def test_organizer_sees_only_own_events_according_to_queryset(
    api_client,
    organizer,
    second_organizer,
    make_event,
):
    own_published = make_event(slug="own-published", is_published=True)
    own_draft = make_event(slug="own-draft", is_published=False)
    foreign_published = make_event(
        organizer=second_organizer,
        title="Foreign Published",
        slug="foreign-published",
        is_published=True,
    )
    api_client.force_authenticate(user=organizer)

    response = api_client.get("/api/events/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert result_ids(response) == [own_published.id, own_draft.id]
    assert foreign_published.id not in result_ids(response)


def test_foreign_organizer_cannot_retrieve_event_hidden_by_queryset(
    api_client,
    second_organizer,
    published_event,
):
    api_client.force_authenticate(user=second_organizer)

    response = api_client.get(f"/api/events/{published_event.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert_error_contract(response, "not_found")


def test_guest_cannot_create_event(api_client, category):
    response = api_client.post(
        "/api/events/",
        event_payload(category),
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert_error_contract(response, "not_authenticated")


def test_attendee_cannot_create_event(api_client, attendee, category):
    api_client.force_authenticate(user=attendee)

    response = api_client.post(
        "/api/events/",
        event_payload(category),
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert_error_contract(response, "permission_denied")


def test_organizer_can_create_event(api_client, organizer, category):
    api_client.force_authenticate(user=organizer)

    response = api_client.post(
        "/api/events/",
        event_payload(category, organizer=organizer.id),
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    created_event = Event.objects.get(slug="drf-meetup")
    assert created_event.organizer == organizer


def test_organizer_can_modify_own_event(api_client, organizer, published_event):
    api_client.force_authenticate(user=organizer)

    response = api_client.patch(
        f"/api/events/{published_event.id}/",
        {"title": "Updated Event"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    published_event.refresh_from_db()
    assert published_event.title == "Updated Event"


def test_attendee_cannot_modify_event(api_client, attendee, published_event):
    api_client.force_authenticate(user=attendee)

    response = api_client.patch(
        f"/api/events/{published_event.id}/",
        {"title": "Blocked Update"},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert_error_contract(response, "permission_denied")
    published_event.refresh_from_db()
    assert published_event.title == "Django Meetup"


def test_organizer_cannot_modify_another_organizers_event(
    api_client,
    second_organizer,
    published_event,
):
    api_client.force_authenticate(user=second_organizer)

    response = api_client.patch(
        f"/api/events/{published_event.id}/",
        {"title": "Foreign Update"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert_error_contract(response, "not_found")
    published_event.refresh_from_db()
    assert published_event.title == "Django Meetup"


def test_attendee_can_register_for_published_event(api_client, attendee, published_event):
    api_client.force_authenticate(user=attendee)

    response = api_client.post(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_200_OK
    assert Registration.objects.filter(
        attendee=attendee,
        event=published_event,
    ).exists()
    assert response.data["event_id"] == published_event.id
    assert response.data["user_id"] == attendee.id


def test_attendee_cannot_register_twice(api_client, attendee, published_event):
    Registration.objects.create(attendee=attendee, event=published_event)
    api_client.force_authenticate(user=attendee)

    response = api_client.post(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert_error_contract(response, "ALREADY_REGISTERED")
    assert Registration.objects.filter(attendee=attendee, event=published_event).count() == 1


def test_attendee_cannot_register_when_capacity_is_full(
    api_client,
    attendee,
    second_attendee,
    make_event,
):
    event = make_event(capacity=1)
    Registration.objects.create(attendee=second_attendee, event=event)
    api_client.force_authenticate(user=attendee)

    response = api_client.post(f"/api/events/{event.id}/register/")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert_error_contract(response, "EVENT_FULL")
    assert not Registration.objects.filter(attendee=attendee, event=event).exists()


def test_cancel_registration_works(api_client, attendee, published_event):
    Registration.objects.create(attendee=attendee, event=published_event)
    api_client.force_authenticate(user=attendee)

    response = api_client.delete(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_200_OK
    assert not Registration.objects.filter(attendee=attendee, event=published_event).exists()


def test_cancel_nonexistent_registration_returns_expected_error(
    api_client,
    attendee,
    published_event,
):
    api_client.force_authenticate(user=attendee)

    response = api_client.delete(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert_error_contract(response, "NOT_REGISTERED")


def test_guest_cannot_register_for_event(api_client, published_event):
    response = api_client.post(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert_error_contract(response, "not_authenticated")


def test_organizer_cannot_register_for_event(api_client, organizer, published_event):
    api_client.force_authenticate(user=organizer)

    response = api_client.post(f"/api/events/{published_event.id}/register/")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert_error_contract(response, "permission_denied")


def test_invalid_event_data_returns_validation_error(api_client, organizer):
    api_client.force_authenticate(user=organizer)

    response = api_client.post(
        "/api/events/",
        {
            "title": "",
            "slug": "",
            "description": "",
            "starts_at": "not-a-date",
            "capacity": 50,
            "is_published": True,
            "organizer": organizer.id,
            "category": 999,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert_error_contract(response, "validation_error")
    assert "title" in response.data["error"]["details"]
    assert "starts_at" in response.data["error"]["details"]
    assert "category" in response.data["error"]["details"]
