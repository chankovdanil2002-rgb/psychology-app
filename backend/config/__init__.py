try:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
except Exception:
    # Celery/Redis not available — tasks will run synchronously
    pass
