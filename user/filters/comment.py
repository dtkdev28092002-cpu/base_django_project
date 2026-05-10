import django_filters
from user.models import Comment


class CommentFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    author_email = django_filters.CharFilter(field_name='author__email', lookup_expr='icontains')
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = ['content', 'author_email', 'post_title']
