from rest_framework import filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from user.models import Tag
from user.serializers import TagSerializer, TagWriteSerializer
from user.filters import TagFilter
from user.auth import IsAdmin
from .pagination import StandardizedModelViewSet, PaginationData


class TagViewSet(StandardizedModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = PaginationData
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TagWriteSerializer
        return TagSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save(user=request.user)
        response_serializer = TagSerializer(tag)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save(user=request.user)
        response_serializer = TagSerializer(tag)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class TagMeListView(StandardizedModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationData
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']
    serializer_class = TagSerializer

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)
