from rest_framework import permissions


class IsAuthenticationCustom(permissions.BasePermission):
    """
    Custom permission class to check if user is authenticated.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """
    Custom permission class to check if user has admin role.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.roles.filter(name='admin').exists()
        )
