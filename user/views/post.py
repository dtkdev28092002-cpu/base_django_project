from rest_framework import filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from user.models import Post
from user.serializers import PostSerializer, PostWriteSerializer
from user.filters import PostFilter
from user.auth import IsAdmin
from .pagination import StandardizedModelViewSet, PaginationData


class PostViewSet(StandardizedModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('author__roles', 'tags')
    pagination_class = PaginationData
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        return PostSerializer

    def _fetch_with_relations(self, pk):
        return Post.objects.select_related('author').prefetch_related('author__roles', 'tags').get(pk=pk)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(
            PostSerializer(self._fetch_with_relations(post.pk)).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        return Response(
            PostSerializer(self._fetch_with_relations(post.pk)).data,
            status=status.HTTP_200_OK
        )


class PostMeListView(StandardizedModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PaginationData
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['-created_at']
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user) \
            .select_related('author').prefetch_related('author__roles', 'tags')
