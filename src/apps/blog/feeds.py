"""Поля для RSS ленты"""
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy

from .models import Article


class LatestArticlesFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:article_list')
    description = 'New posts of my blog.'

    def items(self):
        return Article.objects.filter(status='STATUS_PUBLISHED')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
