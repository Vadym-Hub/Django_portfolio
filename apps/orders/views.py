from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from products.models import Product

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import OrderItem


@require_POST
def cart_add(request, product_id):
    """
    Обработчик добавления товаров в корзину.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    messages.success(request, 'Товар добавлен в корзину.')
    return redirect('orders:cart')


@require_POST
def cart_remove(request, product_id):
    """
    Обработчик для удаления товара из корзины.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'Товар удален с корзины.')
    return redirect('orders:cart')


def cart_detail(request):
    """
    Обработчик товаров, добавленных в корзину.
    """
    cart = Cart(request)
    # Изменение количества товаров
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})

    context = {'cart': cart}
    return render(request, 'shop/cart/cart.html', context)


def order_create(request):
    """
    Обработчик создания заказа.
    """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            messages.success(request, 'Заказ оформлен.')
            context = {'order': order}
            return render(request, 'shop/order/order_created.html', context)
    else:
        form = OrderCreateForm

    messages.success(request, 'Введите данные для оформления заказа.')
    context = {'cart': cart,
               'form': form}
    return render(request, 'shop/order/checkout.html', context)
