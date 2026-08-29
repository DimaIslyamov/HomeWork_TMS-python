class EventRegistrationError(Exception):
    pass


def register_for_event(event, user):
    if event.organizer == user:
        raise EventRegistrationError(
            "Organizer cannot register for own event."
        )

    event.participants.add(user)


def cancel_registration(event, user):
    event.participants.remove(user)
