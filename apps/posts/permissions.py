from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOfComment(BasePermission):
    """
    Автор комментария или записи.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of an object.
        return obj.author == request.user
