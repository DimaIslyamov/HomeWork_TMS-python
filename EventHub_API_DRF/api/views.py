from django.core.serializers import get_serializer
from rest_framework import status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event
from .serializers import EventSerializer


class HealthAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )


class EventListAPIView(
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class EventDetailAPIView(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def patch(self, request, pk):
        return self.partial_update(request, pk)

    def delete(self, request, pk):
       return self.destroy(request, pk)