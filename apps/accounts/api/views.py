from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions

from .serializers import UserSerializer, UserPublicSerializer


User = get_user_model()


class ProfileViewSet(ModelViewSet):
    """
    Обработчик профиля пользователя с проверкой на владельца.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Метод проверяет что пользователь является владельцем.
        """
        return User.objects.filter(id=self.request.user.id)


class ProfilePublicReadOnlyModelViewSet(ReadOnlyModelViewSet):
    """
    Обработчик публичного профиля пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.AllowAny]
