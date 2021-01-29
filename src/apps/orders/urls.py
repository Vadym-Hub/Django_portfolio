from django.urls import path
from . import views


app_name = 'orders'


urlpatterns = [
    # URLs корзины.
    path('cart/', views.cart_detail, name='cart'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    # URLs заказа.
    path('create/', views.order_create, name='order_checkout'),
]
