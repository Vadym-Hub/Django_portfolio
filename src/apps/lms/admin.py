from django.contrib import admin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Регистрация предмета в админке.
    """
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """
    Для отрисовки модуля в админке.
    """
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Регистрация курса в админке.
    """
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]  # Вывод раздела и его регистрация
