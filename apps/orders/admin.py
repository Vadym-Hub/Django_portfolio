from django.contrib import admin

from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Регистрация заказа в админке.
    """
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'phone', 'city', 'address',
                    'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
