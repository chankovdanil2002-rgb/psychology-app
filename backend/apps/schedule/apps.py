"""Конфигурация приложения schedule."""
from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    """Конфигурация приложения schedule."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedule'
    verbose_name = 'Расписание'
