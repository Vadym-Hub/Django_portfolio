from rest_framework import serializers

from base.serializers import RecursiveSerializer, WithoutParentListSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Comment.
    """
    class Meta:
        model = Comment
        fields = (
            "post",
            "text",
            "parent"
        )


class CommentWithoutParentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка комментариев которые не имеют поля parent.
    """
    text = serializers.SerializerMethodField()
    children = RecursiveSerializer(many=True)
    author = serializers.ReadOnlyField(source='author.username')

    def get_text(self, obj):
        """
        Метод возвращает поле text=None если комментарий был удален.
        """
        if obj.deleted:
            return None
        return obj.text

    class Meta:
        list_serializer_class = WithoutParentListSerializer
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "text",
            "created",
            "updated",
            "deleted",
            "children"
        )


class PostSerializer(serializers.ModelSerializer):
    """
    Вывод и редактирование поста.
    """
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentWithoutParentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "created",
            "updated",
            "author",
            "content",
            "comments",
            "comments_count",
            "votes_count"
        )
