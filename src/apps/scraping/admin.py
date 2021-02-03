from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    pass


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    pass
