import django_filters
from .models import Post, Tag, Comment


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Tag
        fields = ['name']

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    tag_ids = django_filters.ModelMultipleChoiceFilter(field_name='tags__id', queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'content', 'author_email', 'tag_ids']

class CommentFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = ['content', 'author_email', 'post_title']