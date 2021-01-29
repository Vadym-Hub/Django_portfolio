from django import template

from ..models import Category, Article

register = template.Library()


@register.simple_tag()
def get_categories():
    """
    Вывод категорий.
    """
    return Category.objects.all()


@register.inclusion_tag('blog/tags/last_articles.html')
def get_last_articles(count=5):
    """
    Вывод последних (по дефолту 5) опубликованных статей.
    """
    articles = Article.objects.filter(status='STATUS_PUBLISHED')[:count]
    return {'last_articles': articles}
