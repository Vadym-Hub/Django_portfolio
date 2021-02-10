from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.urls import reverse

from .fields import OrderField


# Subject 1
#     Course 1
#         Module 1
#             Content 1 (image)
#             Content 2 (text)
#         Module 2
#             Content 3 (text)
#             Content 4 (file)
#             Content 5 (video)
#             ...


class Subject(models.Model):
    """
    Модель предмета.
    """
    title = models.CharField(max_length=200, verbose_name='название предмета')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

    def __str__(self):
        return self.title


class Course(models.Model):
    """
    Модель курса.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='courses_created',
        on_delete=models.CASCADE,
        verbose_name='преподаватель'
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name='предмет'
    )
    title = models.CharField(max_length=200, verbose_name='название курса')
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(verbose_name='описание курса')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания курса')
    updated = models.DateTimeField('обновлено', auto_now=True)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_joined',
        blank=True,
        verbose_name='студенты'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lms:course_detail', kwargs={'slug': self.slug})


class Module(models.Model):
    """
    Модель модуля курса.
    """
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name='курс'
    )
    title = models.CharField(max_length=200, verbose_name='название модуля')
    description = models.TextField(blank=True, verbose_name='описание модуля')
    order = OrderField(blank=True, for_fields=['course'])  # Поле со своим придуманным классом.

    class Meta:
        ordering = ['order']
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """
    Универсальная модель данных которая хранит разные материалы модуля курса.
    Для настройки универсальных отношений необходимы три разных поля(content_type, object_id, item).
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='модуль'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='тип загружаемого контента',
        limit_choices_to={'model__in': ('text', 'video', 'image', 'file')}
    )
    object_id = models.PositiveIntegerField('pk связанного объекта')  # Для хранения первичного ключа связанного объекта.
    item = GenericForeignKey('content_type', 'object_id')  # Поле связанное с объектом с помощью объединения двух предыдущих полей.
    order = OrderField(blank=True, for_fields=['module'])  # Поле со своим придуманным классом

    class Meta:
        ordering = ['order']
        verbose_name = 'содержимое модуля'
        verbose_name_plural = 'содержимое модуля'


class ItemBase(models.Model):
    """
    Абстрактная модель для связей содержимого модуля курса.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_related',  # text_related, file_related, image_related, и video_related
    )
    title = models.CharField('оглавление', max_length=250)
    created = models.DateTimeField('дата создания', auto_now_add=True)
    updated = models.DateTimeField('обновлено', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        """Отображение страницы с содержимым курса в зависимости от типа."""
        return render_to_string(f'lms/manage/module/content/{self._meta.model_name}.html', {'item': self})


class Text(ItemBase):
    """
    Модель текста для модуля курса, наследуэма от ItemBase.
    """
    content = models.TextField('содержание')


class File(ItemBase):
    """
    Модель файла для модуля курса, наследуэма от ItemBase.
    """
    file = models.FileField('файл', upload_to='lms/files')


class Image(ItemBase):
    """
    Модель изображения для модуля курса, наследуэма от ItemBase.
    """
    file = models.FileField('изображение', upload_to='lms/images')


class Video(ItemBase):
    """
    Модель видео для модуля курса, наследуэма от ItemBase.
    """
    url = models.URLField('URL-адрес для видео')
