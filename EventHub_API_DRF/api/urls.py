from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HealthAPIView, EventViewSet


router = DefaultRouter()
router.register("events", EventViewSet, basename="events")

urlpatterns = [
    path("health/", HealthAPIView.as_view(), name="health"),
    path("", include(router.urls)),
]