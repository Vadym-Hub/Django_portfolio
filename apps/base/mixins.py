from rest_framework import mixins, viewsets
from rest_framework.response import Response


class MixedPermissionsForActionsMixin:
    """
    Миксин permissions для action
    """
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CreateUpdateDestroyViewSetMixin(mixins.CreateModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.DestroyModelMixin,
                                      MixedPermissionsForActionsMixin,
                                      viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `update()`, `destroy()`
    actions end mixed permissions for them.
    """
    pass


class CRUDViewSetMixin(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       # mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       MixedPermissionsForActionsMixin,
                       viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `update()`, `destroy()` actions end mixed permissions for them.
    """
    # pass

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
