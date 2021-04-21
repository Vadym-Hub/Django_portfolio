from django.conf import settings
from django.db import models


class Follower(models.Model):
    """
    Модель подписчиков.
    """
    follow = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follow'
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
