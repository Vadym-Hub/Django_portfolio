"""
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'orders.context_processors.cart',  # Добавить в settings.py для отображения контекста корзины.
            ],
        },
    },
]
"""


from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
