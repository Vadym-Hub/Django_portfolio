from rest_framework import permissions, views, response
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins

from .models import Follower
from .serializers import SubscriberListSerializer


User = get_user_model()


class FollowerListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint для списка подписчиков пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscriberListSerializer

    def get_queryset(self):
        return Follower.objects.filter(follow=self.request.user)


class FollowerActionAPIView(views.APIView):
    """
    API endpoint для добавления в подписчики и удаления с подписчиков.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except Follower.DoesNotExist:
            return response.Response(status=404)
        Follower.objects.create(subscriber=request.user, follow=user)
        return response.Response(status=201)

    def delete(self, request, pk):
        try:
            sub = Follower.objects.get(subscriber=request.user, follow_id=pk)
        except Follower.DoesNotExist:
            return response.Response(status=404)
        sub.delete()
        return response.Response(status=204)
