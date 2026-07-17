from rest_framework.permissions import BasePermission


class IsArtist(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "artists"
        )


class IsListener(BasePermission):
        def has_permission(self, request, view):
            return (
                request.user.is_authenticated
                and request.user.role == "listener"
            )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )