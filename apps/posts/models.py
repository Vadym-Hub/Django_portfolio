from django.db import models
from django.conf import settings

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Post(models.Model):
    """
    Модель поста.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор поста',
        related_name='posts'
    )
    content = models.TextField('содержание')
    created = models.DateTimeField('добавлено', auto_now_add=True)
    updated = models.DateTimeField('изменено', auto_now=True)
    votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='votes',
        verbose_name='голосов',
        blank=True
    )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ('-created',)

    def __str__(self):
        return f'id {self.id}'

    def __str__(self):
        return self.content

    def comments_count(self):
        """
        Метод подсчитывает количество комментариев к посту.
        """
        return self.comments.count()

    def votes_count(self):
        """
        Метод подсчитывает количество людей, проголосовавших за пост.
        """
        return self.votes.count()


class Comment(MPTTModel):
    """
    Модель комментария к посту.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='автор комментария',
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='пост',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    text = models.TextField('содержание', max_length=2000)
    created = models.DateTimeField('добавлено', auto_now_add=True)
    updated = models.DateTimeField('изменено', auto_now=True)
    deleted = models.BooleanField('удален', default=False)

    def __str__(self):
        return f'{self.author} - {self.post}: {self.text}'
