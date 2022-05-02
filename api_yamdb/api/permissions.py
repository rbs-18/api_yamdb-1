from rest_framework import permissions


class IsSuperUser(permissions.IsAdminUser):
    """Пермишн проверки суперюзера."""

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrReadOnly(permissions.IsAdminUser):
    """Пермишн для рид-онли, админ с полными правами."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return False


class IsAdmin(permissions.BasePermission):
    """Пермишн для админа."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'admin' or request.user.is_superuser)
        return False


class IsModerator(permissions.BasePermission):
    """Пермишн для модератора."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.role == 'moderator')
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (request.user.role == 'moderator')
        return False


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Пермишн для рид-онли, модератор с полными правами."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'moderator'
