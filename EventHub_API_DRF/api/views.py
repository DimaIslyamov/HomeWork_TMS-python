from rest_framework.response import Response
from rest_framework.views import APIView


class HealthAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )

class EchoAPIView(APIView):
    def post(self, request):
        return Response(
            {
                "received": request.data,
                "query_params": request.query_params,
            }
        )
