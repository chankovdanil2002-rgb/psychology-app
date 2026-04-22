"""Конфигурация Django admin для профилей клиентов."""
from django.contrib import admin

from apps.clients.models import ClientProfile


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    """Админ-представление для ClientProfile."""

    list_display = ('id', 'user', 'first_name', 'last_name', 'is_profile_complete')
    list_filter = ('is_profile_complete',)
    search_fields = ('first_name', 'last_name', 'user__email')
    raw_id_fields = ('user',)
