from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    