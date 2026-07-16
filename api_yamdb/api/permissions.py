from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_staff
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_superuser
        )


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser
