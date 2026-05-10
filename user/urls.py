from django.urls import path

from user.views import (
    HealthCheckView,
    TagViewSet,
    PostViewSet,
    CommentViewSet,
    TagMeListView,
    PostMeListView,
    CommentMeListView,
    UserLoginView,
    UserDetailView,
    RegisterUserView,
    RegisterAdminView,
)

urlpatterns = [
    path("auth/register/user/", RegisterUserView.as_view(), name="register-user"),
    path("auth/register/admin/", RegisterAdminView.as_view(), name="register-admin"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/me/", UserDetailView.as_view(), name="get-me"),
    path("tags/me/", TagMeListView.as_view({"get": "list"}), name="tag-me"),
    path("tags/", TagViewSet.as_view({"get": "list", "post": "create"}), name="tag-list"),
    path("tags/<int:pk>/", TagViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="tag-detail"),
    path("posts/me/", PostMeListView.as_view({"get": "list"}), name="post-me"),
    path("posts/", PostViewSet.as_view({"get": "list", "post": "create"}), name="post-list"),
    path("posts/<int:pk>/", PostViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="post-detail"),
    path("comments/me/", CommentMeListView.as_view({"get": "list"}), name="comment-me"),
    path("comments/", CommentViewSet.as_view({"get": "list", "post": "create"}), name="comment-list"),
    path("comments/<int:pk>/", CommentViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="comment-detail"),
]