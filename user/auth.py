from rest_framework import permissions


class IsAuthenticationCustom(permissions.BasePermission):
    """
    Custom permission class to check if user is authenticated.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if not hasattr(request.user, '_is_admin_cached'):
            request.user._is_admin_cached = request.user.roles.filter(name='admin').exists()
        return request.user._is_admin_cached
