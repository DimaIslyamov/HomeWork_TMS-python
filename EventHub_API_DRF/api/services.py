from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Event, Registration


def register_for_event(*, user, event):
    with transaction.atomic():
        locked_event = Event.objects.select_for_update().get(
            pk=event.pk
        )

        if Registration.objects.filter(
            attendee=user,
            event=locked_event,
        ).exists():
            raise ValidationError(
                {"detail": "User is already registered for this event."}
            )

        registrations_count = locked_event.registrations.count()

        if registrations_count >= locked_event.capacity:
            raise ValidationError(
                {"detail": "Event is full."}
            )

        registration = Registration.objects.create(
            attendee=user,
            event=locked_event,
        )

        return registration


def cancel_registration(*, user, event):
    registration = Registration.objects.filter(
        attendee=user,
        event=event,
    ).first()

    if registration is None:
        raise ValidationError(
            {"detail": "User is not registered for this event."}
        )

    registration.delete()
1