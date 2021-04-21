from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Follower

User = get_user_model()


class SubscriberSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подписчиков.
    """
    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class SubscriberListSerializer(serializers.ModelSerializer):
    subscribers = SubscriberSerializer(many=True, read_only=True)

    class Meta:
        model = Follower
        fields = ('subscribers',)
