from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурация приложения users."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Пользователи'

    def ready(self):
        """Импортирует сигналы при готовности приложения."""
        import apps.users.signals  # noqa: F401
