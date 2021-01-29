"""
Файл для управления виртуальной корзиной покупок.
Чтоб привязать корзину добавте в settings.py:

# Привязка корзины к сессии.
CART_SESSION_ID = 'cart'
"""

from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart(object):
    """
    Класс для работы с корзинами покупок.
    """

    def __init__(self, request):
        """
        Инициализация объекта корзины.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебирает елементы корзины и получает соответствующие
        объекты Product из БД.
        """
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Возвращает общее количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавляет товар в корзину или обновляет его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Сохраняет корзину в сеансе.
        """
        # Отмечаем сеанс как "измененный", чтоб убедится, что он сохранен.
        self.session.modified = True

    def remove(self, product):
        """
        Удаляет товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Очищает сеанс.
        """
        # Удаляем корзину из сеанса.
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """
        Подсчитывает общую стоимость корзины.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_quantity(self):
        """
        Подсчитывает общее количество товара в корзине.
        """
        return sum(int(item['quantity']) for item in self.cart.values())
