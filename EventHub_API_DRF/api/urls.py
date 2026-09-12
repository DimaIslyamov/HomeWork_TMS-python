from django.urls import path

from .views import HealthAPIView, EventListAPIView, EventDetailAPIView

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health"),
    path("events/", EventListAPIView.as_view(), name="event-list"),

    path("events/<int:pk>/", EventDetailAPIView.as_view(), name="event-detail"),
]