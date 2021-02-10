from django import template
from ..models import Category


register = template.Library()


@register.simple_tag()
def get_categories():
    """
    Вывод категорий товара.
    """
    return Category.objects.all()
