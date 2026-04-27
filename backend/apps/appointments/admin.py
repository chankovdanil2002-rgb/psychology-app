"""Настройка административного интерфейса для приложения appointments."""
from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Административное представление модели Appointment."""

    list_display = ('id', 'client', 'psychologist', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = (
        'client__first_name',
        'client__last_name',
        'psychologist__first_name',
        'psychologist__last_name',
    )
    raw_id_fields = ('client', 'psychologist', 'time_slot')
    readonly_fields = ('created_at', 'updated_at')
