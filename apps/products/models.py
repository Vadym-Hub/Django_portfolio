from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Модель категории.
    """
    name = models.CharField(max_length=200, db_index=True, verbose_name='название категории')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """
    Модель товара.
    """
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='изображение')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    stock = models.PositiveIntegerField(verbose_name='количество')
    available = models.BooleanField(default=True, verbose_name='в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='обновлено')

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'id': self.id,
                                                          'slug': self.slug})
