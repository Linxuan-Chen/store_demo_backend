from rest_framework import permissions


class IsAdminOrAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff) #type ignore
