from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Сериализатор для публичной информации о user.
    """
    class Meta:
        model = User
        exclude = (
            "email",
            "mobile_phone",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
            "send_email",
            "is_organisor",
            "is_agent",
        )


class UserByFollowerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписчиков.
    """
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')
