from rest_framework import permissions


class ReadOnlyPermission(permissions.BasePermission):
    """Разрешение безопасных запросов для анонимных пользователей"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class AdminOnly(permissions.BasePermission):
    """Разрешение запросов только для администратора"""

    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )
