"""
Настройки режима разработки приложения записи к психологу.
"""
from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'psychology_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ──────────────────────────────────────────────
# Email — в режиме разработки письма выводятся в консоль
# ──────────────────────────────────────────────

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend',
)

# ──────────────────────────────────────────────
# Кэш — в оперативной памяти процесса (локальный dev-кэш)
# ──────────────────────────────────────────────

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'psychology-app-dev-cache',
    }
}

# ──────────────────────────────────────────────
# CORS — в режиме разработки разрешаем все источники
# ──────────────────────────────────────────────

CORS_ALLOW_ALL_ORIGINS = True

# ──────────────────────────────────────────────
# DRF — включаем браузерный API-интерфейс для разработки
# ──────────────────────────────────────────────

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (  # noqa: F405
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

