from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer,
)
from rest_framework import serializers

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

    @extend_schema(
        responses=inline_serializer(
            name="HealthResponse",
            fields={
                "status": serializers.CharField(),
                "message": serializers.CharField(),
            },
        )
    )
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )


class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        event_pk = self.kwargs["event_pk"]
        
        return Session.objects.filter(event_id=event_pk)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Order by starts_at or title. Prefix with '-' for descending order.",
            ),
        ]
    )
)
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
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

    @extend_schema(
        request=None,
        methods=["POST"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="RegistrationCreatedResponse",
                    fields={
                        "message": serializers.CharField(),
                        "registration_id": serializers.IntegerField(),
                        "event_id": serializers.IntegerField(),
                        "user_id": serializers.IntegerField(),
                    },
                ),
                description="Registration created successfully",
            )
        },
    )
    @extend_schema(
        request=None,
        methods=["DELETE"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="RegistrationCanceledResponse",
                    fields={
                        "message": serializers.CharField(),
                    },
                ),
                description="Registration canceled successfully",
            )
        }
    )
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
