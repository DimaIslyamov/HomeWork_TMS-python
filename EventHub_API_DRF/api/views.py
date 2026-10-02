from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Session
from .permissions import IsOrganizer, IsEventOwner, IsAttendee
from .pagination import EventPagination
from .serializers import EventSerializer, SessionSerializer
from .services import register_for_event, cancel_registration


class HealthAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )


class SessionViewSet(ModelViewSet):
    serializer_class = SessionSerializer

    def get_queryset(self):
        event_pk = self.kwargs["event_pk"]
        
        return Session.objects.filter(event_id=event_pk)


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = EventPagination
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ["category", "is_published"]
    search_fields = ["title", "description"]
    ordering_fields = ["starts_at", "title"]

    def get_queryset(self):
        user = self.request.user

        if self.action == "list":
            if not user.is_authenticated:
                return Event.objects.filter(
                    is_published=True
                ).prefetch_related("sessions")
            if user.role == "ATTENDEE":
                return Event.objects.filter(
                    is_published=True
                ).prefetch_related("sessions")
            if user.role == "ORGANIZER":
                return Event.objects.filter(
                    organizer=user
                ).prefetch_related("sessions")

        if self.action == "retrieve":
            if not user.is_authenticated:
                return Event.objects.filter(is_published=True)
            if user.role == "ATTENDEE":
                return Event.objects.filter(is_published=True)
            if user.role == "ORGANIZER":
                return Event.objects.filter(organizer=user)

        if self.action == "register":
            return Event.objects.filter(is_published=True)

        if self.action in ["update", "partial_update", "destroy"]:
            return Event.objects.filter(organizer=user)

        return Event.objects.none()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        if self.action == "create":
            return [IsOrganizer()]
        if self.action == "register":
            return [IsAttendee()]

        return [IsOrganizer(), IsEventOwner()]

    @action(detail=True, methods=["post", "delete"])
    def register(self, request, pk=None):
        event = self.get_object()

        if request.method == "POST":
            registration = register_for_event(
                user=request.user,
                event=event,
            )
            return Response({
                "message": "Registration created",
                "registration_id": registration.id,
                "event_id": event.id,
                "user_id": request.user.id,
            })

        if request.method == "DELETE":
            cancel_registration(
                user=request.user,
                event=event,
            )

            return Response({
                "message": "Registration canceled"
            })
