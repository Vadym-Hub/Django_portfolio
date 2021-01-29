from django.shortcuts import get_object_or_404
from django.views import generic
from orders.forms import CartAddProductForm

from .models import Product, Category


class ProductListView(generic.ListView):
    """
    Обработчик вывода списка всех товаров и товаров по категории.
    """
    template_name = 'shop/product/product_list.html'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        category = None
        queryset = Product.objects.filter(available=True)
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset


class ProductDetailView(generic.DetailView):
    """
    Обработчик вывода информации конкретного товара.
    """
    template_name = 'shop/product/product_detail.html'
    queryset = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'cart_product_form': self.cart_product_form
        })
        return context
