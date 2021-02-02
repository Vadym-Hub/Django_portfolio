from django import template

from ..models import Subject

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.simple_tag()
def get_subjects():
    """
    Вывод категорий.
    """
    return Subject.objects.all()
