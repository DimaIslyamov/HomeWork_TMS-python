from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Event
from .permissions import IsOrganizer, IsEventOwner
from .serializers import EventSerializer


class HealthAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )


class EventViewSet(ModelViewSet):
    # queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsOrganizer, IsEventOwner]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        if self.action == "create":
            return [IsOrganizer()]

        return [IsOrganizer(), IsEventOwner()]

    def get_queryset(self):
        user = self.request.user

        if self.action in ["list", "retrieve"]:
            if not user.is_authenticated:
                return Event.objects.filter(is_published=True)

            if user.role == "ATTENDEE":
                return Event.objects.filter(is_published=True)

            if user.role == "ORGANIZER":
                return Event.objects.filter(organizer=user)

        if self.action in ["update", "partial_update", "destroy"]:
            return Event.objects.filter(organizer=user)

        return Event.objects.none()

