from django.contrib import admin
from .models import Article, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в админке"""
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Отображение статьи в админке"""
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body', 'author__username', 'category')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение коментариев в админке"""
    pass
