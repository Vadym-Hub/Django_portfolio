from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


User = get_user_model()


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
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


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для встроеной модели Group.
    """
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Вывод аватара пользователя
    """
    class Meta:
        model = User
        fields = ("avatar",)


# class UserPublicSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор для публичной информации о user.
#     """
#     class Meta:
#         model = User
#         exclude = (
#             "email",
#             "mobile_phone",
#             "password",
#             "last_login",
#             "is_active",
#             "is_staff",
#             "is_superuser",
#             "groups",
#             "user_permissions",
#             "send_email",
#             "is_organisor",
#             "is_agent",
#         )
