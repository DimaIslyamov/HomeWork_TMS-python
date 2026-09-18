from accounts.views import RegisterAPIView

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import HealthAPIView, EventViewSet


router = DefaultRouter()
router.register("events", EventViewSet, basename="events")

urlpatterns = [
    path("health/", HealthAPIView.as_view()),

    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/token/", TokenObtainPairView.as_view()),
    path("auth/token/refresh/", TokenRefreshView.as_view()),

    path("", include(router.urls)),
]
