from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Вывод постов в админке.
    """
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Вывод комментариев к посту в админке.
    """
    pass
