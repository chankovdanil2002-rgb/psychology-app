"""
Продакшн-настройки для приложения записи к психологу.

Читает чувствительные значения из переменных окружения.
"""
import os

import dj_database_url

from .base import *  # noqa: F401, F403

# ──────────────────────────────────────────────
# Безопасность
# ──────────────────────────────────────────────

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Настройки HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ──────────────────────────────────────────────
# База данных — PostgreSQL через DATABASE_URL
# ──────────────────────────────────────────────

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ──────────────────────────────────────────────
# Кэш — Redis
# ──────────────────────────────────────────────

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
        'TIMEOUT': 600,
    }
}

# ──────────────────────────────────────────────
# Статические файлы
# ──────────────────────────────────────────────

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# ──────────────────────────────────────────────
# CORS — ограниченный список источников
# ──────────────────────────────────────────────

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS', ''
).split(',')

# ──────────────────────────────────────────────
# Логирование — продакшн-уровень
# ──────────────────────────────────────────────

LOGGING['root']['level'] = 'WARNING'  # noqa: F405
LOGGING['loggers']['django']['level'] = 'WARNING'  # noqa: F405
LOGGING['loggers']['ap']['level'] = 'INFO'  # noqa: F405
