from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import TagFilter
from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TagFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Default ordering by newest first
