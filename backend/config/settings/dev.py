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

# Email-настройки берутся из .env (EMAIL_BACKEND, EMAIL_HOST_USER и т.д.)

# ──────────────────────────────────────────────
# Кэш — файловый (разделяется между процессами, подходит для dev)
# ──────────────────────────────────────────────

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / '.dev_cache',  # noqa: F405
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

