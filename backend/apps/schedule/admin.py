"""Настройка административного интерфейса для приложения schedule."""
from django.contrib import admin

from .models import TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Административное представление модели TimeSlot."""

    list_display = ('psychologist', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'date')
    search_fields = (
        'psychologist__first_name',
        'psychologist__last_name',
    )
    raw_id_fields = ('psychologist',)
