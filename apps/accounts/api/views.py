from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, response, mixins
from PIL import Image

from .permissions import IsOwnerProfileOrReadOnly, IsOwner
from .serializers import ProfileSerializer, GroupSerializer, UserAvatarSerializer


User = get_user_model()


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint для модели User.
    Позволяет `retrieve()`, 'list()',
    `update()`, `partial_update()` , `destroy()`
    действия для хозяина профиля.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly]
    queryset = User.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class ProfileAvatarAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint для изменения аватара пользователя.
    """
    serializer_class = UserAvatarSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        max_weight = 1048576
        min_size = 100
        max_size = 5000
        try:
            avatar = request.data["avatar"]
            image = Image.open(avatar)
            (width, height) = image.size
            if avatar.size > max_weight:
                return response.Response({"error": "Please upload a picture smaller than 1 MB."}, status=400)
            elif width and height < min_size:
                return response.Response({"error": "Please upload a picture bigger than {}x{}."
                                         .format(min_size, min_size)}, status=400)
            elif width and height > max_size:
                return response.Response({"error": "Please upload a picture smaller than {}x{}."
                                         .format(max_size, max_size)}, status=400)
            # можно удалить старую аватарку без сигналов
            # else:
            #     image = request.user.avatar.path
            #     if os.path.exists(image):
            #         os.remove(image)
            #     else:
            #         return response.Response({"error": "File does not exists."}, status=400)
        except KeyError:
            response.Response(status=400)
        return self.update(request, avatar=avatar)
