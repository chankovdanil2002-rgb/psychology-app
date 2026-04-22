"""Конфигурация Django-приложения psychologists."""
from django.apps import AppConfig


class PsychologistsConfig(AppConfig):
    """Конфигурация приложения psychologists."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.psychologists'
    verbose_name = 'Psychologists'
