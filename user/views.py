from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from .filters import CommentFilter, PostFilter, TagFilter
from .models import Tag, Post, Comment
from .serializers import (
    TagSerializer,
    PostSerializer,
    CommentSerializer,
    RegisterUserSerializer,
    RegisterAdminSerializer,
    LoginSerializer,
    TagWriteSerializer,
    UserDetailSerializer,
    UserSerializer,
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
    pagination_class = TagPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = [
        'name',
        'created_at',
        'updated_at'
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in [
            'create',
            'update',
            'partial_update'
        ]:
            return TagWriteSerializer
        return TagSerializer

    def get_permissions(self):
        if self.action in [
            'update',
            'partial_update',
            'destroy'
        ]:
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

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = TagPagination
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
            from .serializers import PostWriteSerializer
            return PostWriteSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        response_serializer = PostSerializer(post)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)
        response_serializer = PostSerializer(post)
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = TagPagination
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
            from .serializers import CommentWriteSerializer
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


class TagMeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Tag.objects.filter(user=request.user)
        paginator = TagPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = TagSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class PostMeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Post.objects.filter(author=request.user)
        paginator = TagPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = PostSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CommentMeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Comment.objects.filter(author=request.user)
        paginator = TagPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
class RegisterAdminView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterAdminSerializer)
    def post(self, request):
        serializer = RegisterAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'Service is running',
        }, status=status.HTTP_200_OK)
