"""Application configuration for the schedule app."""
from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    """Configuration for the schedule app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.schedule'
    verbose_name = 'Schedule'
