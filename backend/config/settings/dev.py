"""
Настройки режима разработки приложения записи к психологу.

DEBUG=True, PostgreSQL (или SQLite как запасной вариант), email в консоль.
"""
from .base import *  # noqa: F401, F403

# ──────────────────────────────────────────────
# Режим отладки
# ──────────────────────────────────────────────

DEBUG = True

ALLOWED_HOSTS = ['*']

# ──────────────────────────────────────────────
# База данных
# По умолчанию — PostgreSQL (совпадает с docker-compose: localhost:5432).
# Если переменная окружения USE_SQLITE=1 — используется локальный SQLite-файл
# (удобно, когда PostgreSQL ещё не запущен).
# ──────────────────────────────────────────────

if os.environ.get('USE_SQLITE') == '1':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
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

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

# ──────────────────────────────────────────────
# Celery — в dev-режиме выполняем задачи синхронно, без брокера
# ──────────────────────────────────────────────

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
