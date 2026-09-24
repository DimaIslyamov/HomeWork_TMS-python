from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Session
from .permissions import IsOrganizer, IsEventOwner
from .pagination import EventPagination
from .serializers import EventSerializer, SessionSerializer


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

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        if self.action == "create":
            return [IsOrganizer()]

        return [IsOrganizer(), IsEventOwner()]
