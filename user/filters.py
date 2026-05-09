import django_filters
from .models import Tag


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']