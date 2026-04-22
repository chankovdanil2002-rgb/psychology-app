"""Application configuration for the specializations app."""
from django.apps import AppConfig


class SpecializationsConfig(AppConfig):
    """Configuration for the specializations app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.specializations'
    verbose_name = 'Specializations'
