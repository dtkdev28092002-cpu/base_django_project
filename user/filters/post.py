import django_filters
from user.models import Post, Tag


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    tag_ids = django_filters.ModelMultipleChoiceFilter(field_name='tags__id', queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'content', 'author_email', 'tag_ids']
