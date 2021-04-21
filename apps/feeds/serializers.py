from rest_framework import serializers

from posts.models import Post


class PostForFeedSerializer(serializers.ModelSerializer):
    """ Список постов
    """
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ("id", "created", "author", "content", "comments_count", "votes_count")
