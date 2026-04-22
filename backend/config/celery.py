"""
Конфигурация Celery для приложения записи к психологу.
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('psychology_app')

# Загружаем настройки задач из всех зарегистрированных Django-приложений.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматический поиск задач во всех установленных приложениях (ищет tasks.py в каждом).
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Отладочная задача, печатающая информацию о текущем запросе."""
    print(f'Request: {self.request!r}')
