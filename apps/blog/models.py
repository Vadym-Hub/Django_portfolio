from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class Category(models.Model):
    """
    Модель категорий.
    """
    name = models.CharField('название', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:article_list_by_category', kwargs={'slug': self.slug})


class Article(models.Model):
    """
    Модель статьи.
    """

    STATUS_DRAFT = 'STATUS_DRAFT'
    STATUS_PUBLISHED = 'STATUS_PUBLISHED'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PUBLISHED, 'Опубликовано'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='категория',
    )
    title = models.CharField('заголовок', max_length=200)
    slug = models.SlugField(unique_for_date='publish', unique=True)
    poster = models.ImageField('постер', upload_to='articles/%Y/%m/%d/', blank=True, null=True)
    description = models.TextField('краткое описание', blank=True)
    content = models.TextField('содержание')
    status = models.CharField('статус', max_length=20, choices=STATUS_CHOICES, default='STATUS_DRAFT')
    allow_comments = models.BooleanField('комменты розрешены', default=True)
    publish = models.DateTimeField('опубликовано', default=timezone.now)
    created = models.DateTimeField('создано', auto_now_add=True)
    updated = models.DateTimeField('обновлено', auto_now=True)
    previous_article = models.ForeignKey(
        'self',
        related_name='previous',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='предыдущая часть')
    next_article = models.ForeignKey(
        'self',
        related_name='next',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='следующая часть')

    tags = TaggableManager()

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(article=self).count()


class Comment(models.Model):
    """
    Модель комментария.
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='статья'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='автор комментария',
        on_delete=models.CASCADE
    )
    content = models.TextField('содержание')
    timestamp = models.DateTimeField('время', auto_now_add=True)

    class Meta:
        verbose_name = 'комментар'
        verbose_name_plural = 'комментарии'

    def get_absolute_url(self):
        return reverse('blog:article_detail')

    def __str__(self):
        return f'{self.author}'
