from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .pagination import StandardizedAPIView


class HealthCheckView(StandardizedAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'message': 'Service is running',
            'data': {'status': 'ok'},
        }, status=status.HTTP_200_OK)
