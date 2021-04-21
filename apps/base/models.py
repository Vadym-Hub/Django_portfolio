from django.db import models

# from mptt.fields import TreeForeignKey
# from mptt.models import MPTTModel

from .services import from_cyrillic_to_eng


class HardSkill(models.Model):
    """
    Модель хард скила.
    """

    name = models.CharField('название навыка', max_length=100, unique=True)

    class Meta:
        verbose_name = 'hard skill'
        verbose_name_plural = 'hard skills'

    def __str__(self):
        return self.name


class SoftSkill(models.Model):
    """
    Модель софт скила.
    """
    name = models.CharField('название', max_length=100, unique=True)

    class Meta:
        verbose_name = 'soft skill'
        verbose_name_plural = 'soft skills'

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Модель города.
    """
    name = models.CharField('название', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

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


# class AbstractMPTTModel(MPTTModel):
#     """
#     Абстрактная, древовидная модель.
#     Поля: text, parent, created, updated, deleted.
#     """
#     text = models.TextField('содержание', max_length=2000)
#     created = models.DateTimeField('добавлено', auto_now_add=True)
#     updated = models.DateTimeField('изменено', auto_now=True)
#     deleted = models.BooleanField('удален', default=False)
#     parent = TreeForeignKey(
#         'self',
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name='children'
#     )
#
#     def __str__(self):
#         return f'{self.text}'
#
#     class Meta:
#         abstract = True
