from celery import shared_task

from .models import Registration


@shared_task
def test_task():
    print("Celery task executed")


@shared_task
def registration_confirmation_task(registration_id):
    registration = Registration.objects.get(id=registration_id)

    print(
        f"Registration confirmed: "
        f"user={registration.attendee_id}, "
        f"event={registration.event_id}"
    )


@shared_task(bind=True, max_retries=2)
def test_retry_task(self):
    print(f"Attempt: {self.request.retries + 1}")

    if self.request.retries < 2:
        raise self.retry(countdown=5)

    print("Task completed successfully")