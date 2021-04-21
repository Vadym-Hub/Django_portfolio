from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Автор записи.
    """
    def has_object_permission(self, request, view, obj):
        return bool(obj.id == request.user.id)


class IsOwnerProfileOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(obj.id == request.user.id)


# class IsOwnerProfileOrReadOnlyIsAuthenticated(BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `user` attribute.
#     """
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return bool(obj.id == request.user.id)
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)
