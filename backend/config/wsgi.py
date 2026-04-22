"""
Конфигурация WSGI для приложения записи к психологу.

Экспортирует WSGI-вызываемое как переменную уровня модуля с именем ``application``.

Подробнее об этом файле см.
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
