from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint для модели Post.
    """
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def upvote(self, request, *args, **kwargs):
        """
        API endpoint для голосования за пост.
        """
        post = self.get_object()
        if post.votes.filter(id=self.request.user.id).exists():
            post.votes.remove(self.request.user)
            return Response(status=201)
        post.votes.add(self.request.user)
        return Response(status=201)


class CommentViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint для модели комментариев.
    """
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        """
        При удалении коммента ставится поле deleted=True.
        Нужно для вывода древа комментариев даже если коммент удален.
        """
        instance.deleted = True
        instance.save()
