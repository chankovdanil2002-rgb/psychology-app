"""Настройка административного интерфейса для приложения reviews."""
from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Административное представление модели Review."""

    list_display = ('id', 'appointment', 'rating', 'created_at')
    list_filter = ('rating',)
    raw_id_fields = ('appointment',)
    readonly_fields = ('created_at',)
