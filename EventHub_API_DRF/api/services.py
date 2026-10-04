from django.db import transaction
from rest_framework.exceptions import ValidationError

from .exceptions import EventFullError, AlreadyRegisteredError, NotRegisteredError
from .models import Event, Registration
from .tasks import registration_confirmation_task


def register_for_event(*, user, event):
    with transaction.atomic():
        locked_event = Event.objects.select_for_update().get(
            pk=event.pk
        )

        if Registration.objects.filter(
            attendee=user,
            event=locked_event,
        ).exists():
            raise AlreadyRegisteredError()

        registrations_count = locked_event.registrations.count()

        if registrations_count >= locked_event.capacity:
            raise EventFullError()

        registration = Registration.objects.create(
            attendee=user,
            event=locked_event,
        )

        transaction.on_commit(
            lambda: registration_confirmation_task.delay(registration.id)
        )

        return registration


def cancel_registration(*, user, event):
    registration = Registration.objects.filter(
        attendee=user,
        event=event,
    ).first()

    if registration is None:
        raise NotRegisteredError()

    registration.delete()
