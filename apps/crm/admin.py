from django.contrib import admin

from .models import Lead, Agent, Organisation


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    """Отображение организации юзера в админке."""
    pass


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    """Отображение агента в админке."""
    pass


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Отображение лида в админке."""
    pass

