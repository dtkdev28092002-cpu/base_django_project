from django.urls import path

from .views import HealthCheckView, TagViewSet, UserLoginView, UserDetailView, RegisterUserView, RegisterAdminView

urlpatterns = [
    path("auth/register/user/", RegisterUserView.as_view(), name="register-user"),
    path("auth/register/admin/", RegisterAdminView.as_view(), name="register-admin"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/me/", UserDetailView.as_view(), name="get-me"),
    path("tags/", TagViewSet.as_view({"get": "list", "post": "create"}), name="tag-list"),
    path("tags/<int:pk>/", TagViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="tag-detail"),
]