from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from .filters import TagFilter
from .models import Tag
from .serializers import (
    TagSerializer, 
    RegisterUserSerializer,
    RegisterAdminSerializer,
    LoginSerializer, 
    UserDetailSerializer
)
from .auth import IsAdmin


class TagPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        from math import ceil
        total_pages = ceil(self.page.paginator.count / self.get_page_size(self.request)) if self.page.paginator.count > 0 else 1
        return Response({
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total_page': total_pages,
            "total_count": self.page.paginator.count,
            'results': data
        })


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = TagPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering by newest first

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(
            serializer.response(user),
            status=status.HTTP_200_OK
        )
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'username': user.username,
            },
        }, status=status.HTTP_201_CREATED)
    
class RegisterAdminView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterAdminSerializer)
    def post(self, request):
        serializer = RegisterAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'username': user.username,
            },
        }, status=status.HTTP_201_CREATED)


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'Service is running',
        }, status=status.HTTP_200_OK)
