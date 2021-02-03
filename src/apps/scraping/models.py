from django.db import models

from .services import from_cyrillic_to_eng


def default_urls():
    """
    Передача урлов для таблицы URL.
    """
    return {"work": "", "rabota": "", "dou": "", "djinni": ""}


class City(models.Model):
    """
    Модель города где ищем вакансию.
    """
    name = models.CharField('название', max_length=50, unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Метод автоматически заполняет поле slug если оно пустое.
        """
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    """
    Модель языка программирования.
    """
    name = models.CharField('язык программирования', max_length=50, unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'язык программирования'
        verbose_name_plural = 'языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Метод автоматически заполняет поле slug если оно пустое.
        """
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    """
    Модель для сохранения найденой вакансии.
    """
    url = models.URLField(unique=True)
    title = models.CharField('заголовок вакансии', max_length=250)
    company = models.CharField('компания', max_length=250)
    description = models.TextField('описание вакансии')
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='город'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name='язык программирования'
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'вакансия'
        verbose_name_plural = 'вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    """
    Модель для сбора ошибок.
    """
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    """
    Модель для сбора урлов.
    """
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name='город'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name='язык программирования'
    )
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'language')
