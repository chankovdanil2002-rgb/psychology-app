"""Application configuration for the appointments app."""
from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Configuration for the appointments app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.appointments'
    verbose_name = 'Appointments'
