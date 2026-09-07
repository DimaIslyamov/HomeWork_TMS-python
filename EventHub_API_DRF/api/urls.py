from django.urls import path

from .views import HealthAPIView, EchoAPIView


urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health"),
    path("echo/", EchoAPIView.as_view(), name="echo"),
]