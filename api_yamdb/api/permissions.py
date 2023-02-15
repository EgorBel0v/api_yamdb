from rest_framework import permissions


class ReadOnlyPermission(permissions.BasePermission):
    """Разрешение безопасных запросов для анонимных пользователей"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminPermission(permissions.BasePermission):
    """Разрешение запросов только для администратора"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
