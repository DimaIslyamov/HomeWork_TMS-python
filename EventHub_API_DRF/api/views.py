from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EchoSerializer


class HealthAPIView(APIView):
    def get(self, request):
        return Response(
            {
                'status': 'ok',
                'message': 'EventHub API is running',
            }
        )

# class EchoAPIView(APIView):
#     def post(self, request):
#         return Response(
#             {
#                 "received": request.data,
#                 "query_params": request.query_params,
#             }
#         )

class EchoAPIView(APIView):
    def post(self, request):
        serializer = EchoSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                {
                    "validated_data": serializer.validated_data,
                }
            )

        return Response(
            {
                "errors": serializer.errors,
            },
            status=400,
        )