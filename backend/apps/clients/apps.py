"""Конфигурация Django-приложения clients."""
from django.apps import AppConfig


class ClientsConfig(AppConfig):
    """Конфигурация приложения clients."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clients'
    verbose_name = 'Clients'
