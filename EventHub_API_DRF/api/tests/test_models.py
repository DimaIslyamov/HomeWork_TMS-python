import pytest
from django.db import IntegrityError

from api.models import Registration


pytestmark = pytest.mark.django_db


def test_event_capacity_must_be_positive(make_event):
    with pytest.raises(IntegrityError):
        make_event(capacity=0)


def test_registration_is_unique_per_event_and_attendee(attendee, published_event):
    Registration.objects.create(attendee=attendee, event=published_event)

    with pytest.raises(IntegrityError):
        Registration.objects.create(attendee=attendee, event=published_event)
