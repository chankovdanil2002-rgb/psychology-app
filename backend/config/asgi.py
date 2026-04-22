"""
Конфигурация ASGI для приложения записи к психологу.

Экспортирует ASGI-вызываемое как переменную уровня модуля с именем ``application``.

Подробнее об этом файле см.
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_asgi_application()
