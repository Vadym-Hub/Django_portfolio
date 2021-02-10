from django.db import models

from products.models import Product


class Order(models.Model):
    """
    Модель заказа.
    """
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    first_name = models.CharField(max_length=50, verbose_name='имя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия')
    email = models.EmailField(verbose_name='e-mail')
    phone = models.CharField(max_length=15, verbose_name='телефон')
    city = models.CharField(max_length=100, verbose_name='город')
    address = models.CharField(max_length=250, verbose_name='адресс')
    comment = models.TextField(verbose_name='комментарий к заказу', null=True, blank=True)
    paid = models.BooleanField(default=False, verbose_name='оплачено')
    status = models.CharField(max_length=100,
                              choices=STATUS_CHOICES,
                              default=STATUS_NEW,
                              verbose_name='статус заказ')
    buying_type = models.CharField(max_length=100,
                                   choices=BUYING_TYPE_CHOICES,
                                   default=BUYING_TYPE_SELF,
                                   verbose_name='тип заказа')
    braintree_id = models.CharField(max_length=150, blank=True, verbose_name='идентификатор транзакции')
    created = models.DateTimeField(auto_now_add=True, verbose_name='время оформления')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        """Возвращает общую стоимость товаров в заказе."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Модель для связи заказа с покупаемыми товарами и указания их стоимости и количества.
    """
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,
                              verbose_name='заказ')
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE,
                                verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        """Возвращает стоимость количества товара."""
        return self.price * self.quantity
