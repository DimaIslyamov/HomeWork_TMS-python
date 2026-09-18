from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def test_registration_rejects_password_blocked_by_django_validators(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "weak_password_user",
                "email": "weak@example.com",
                "password": "password",
                "role": "ATTENDEE",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(
            get_user_model().objects.filter(username="weak_password_user").exists()
        )
