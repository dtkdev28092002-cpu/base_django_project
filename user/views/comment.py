from rest_framework import filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from user.models import Comment
from user.serializers import CommentSerializer, CommentWriteSerializer
from user.filters import CommentFilter
from user.auth import IsAdmin
from .pagination import StandardizedModelViewSet, PaginationData


class CommentViewSet(StandardizedModelViewSet):
    queryset = Comment.objects.all()
    pagination_class = PaginationData
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentWriteSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user)
        response_serializer = CommentSerializer(comment)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user)
        response_serializer = CommentSerializer(comment)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class CommentMeListView(StandardizedModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationData
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = CommentFilter
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)
