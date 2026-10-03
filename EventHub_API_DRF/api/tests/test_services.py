import pytest

from api.exceptions import AlreadyRegisteredError, EventFullError, NotRegisteredError
from api.models import Registration
from api.services import cancel_registration, register_for_event


pytestmark = pytest.mark.django_db


def test_register_for_event_creates_registration(attendee, published_event):
    registration = register_for_event(user=attendee, event=published_event)

    assert registration.attendee == attendee
    assert registration.event_id == published_event.id
    assert Registration.objects.filter(attendee=attendee, event=published_event).exists()


def test_register_for_event_rejects_duplicate_registration(attendee, published_event):
    Registration.objects.create(attendee=attendee, event=published_event)

    with pytest.raises(AlreadyRegisteredError) as exc_info:
        register_for_event(user=attendee, event=published_event)

    assert exc_info.value.get_codes() == "ALREADY_REGISTERED"
    assert Registration.objects.filter(attendee=attendee, event=published_event).count() == 1


def test_register_for_event_rejects_full_event(
    attendee,
    second_attendee,
    make_event,
):
    event = make_event(capacity=1)
    Registration.objects.create(attendee=second_attendee, event=event)

    with pytest.raises(EventFullError) as exc_info:
        register_for_event(user=attendee, event=event)

    assert exc_info.value.get_codes() == "EVENT_FULL"
    assert not Registration.objects.filter(attendee=attendee, event=event).exists()


def test_cancel_registration_removes_existing_registration(attendee, published_event):
    Registration.objects.create(attendee=attendee, event=published_event)

    cancel_registration(user=attendee, event=published_event)

    assert not Registration.objects.filter(attendee=attendee, event=published_event).exists()


def test_cancel_registration_rejects_missing_registration(attendee, published_event):
    with pytest.raises(NotRegisteredError) as exc_info:
        cancel_registration(user=attendee, event=published_event)

    assert exc_info.value.get_codes() == "NOT_REGISTERED"
