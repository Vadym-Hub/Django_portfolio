from django import forms

from .models import Order


# Позволяет пользователю выбрать количество между 1-20.
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """
    Форма для добавления товара в корзину.
    """
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    """
    Форма для подробностей заказа.
    """
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email',
                  'phone', 'city', 'address', 'buying_type', 'comment']
