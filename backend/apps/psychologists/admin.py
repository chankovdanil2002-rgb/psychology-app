"""Конфигурация Django admin для профилей психологов."""
from django.contrib import admin

from apps.psychologists.models import PsychologistProfile


@admin.register(PsychologistProfile)
class PsychologistProfileAdmin(admin.ModelAdmin):
    """Админ-представление для PsychologistProfile."""

    list_display = (
        'id',
        'user',
        'first_name',
        'last_name',
        'is_verified',
        'is_profile_complete',
        'price',
    )
    list_filter = ('is_verified', 'is_profile_complete')
    search_fields = ('first_name', 'last_name', 'patronymic', 'user__email')
    raw_id_fields = ('user',)
    readonly_fields = ('verified_at',)
