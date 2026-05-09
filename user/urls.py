from django.urls import path

from .views import TagViewSet

urlpatterns = [
    path("tags/", TagViewSet.as_view({"get": "list", "post": "create"}), name="tag-list"),
    path("tags/<int:pk>/", TagViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="tag-detail"),
]