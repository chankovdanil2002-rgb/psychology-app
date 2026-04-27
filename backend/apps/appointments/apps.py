"""Конфигурация приложения appointments."""
from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Конфигурация приложения appointments."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appointments'
    verbose_name = 'Записи на приём'
