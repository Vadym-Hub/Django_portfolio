from django.contrib import admin

from .models import HardSkill, SoftSkill, City


@admin.register(HardSkill)
class HardSkillAdmin(admin.ModelAdmin):
    """Хард скилы в админке."""
    pass


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    """Софт скилы в админке."""
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Города в админке."""
    pass
