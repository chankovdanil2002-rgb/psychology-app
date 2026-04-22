"""
URL-конфигурация для эндпоинтов профиля.
"""
from django.urls import path

from apps.users.views import ProfileMeView

app_name = 'clients'

urlpatterns = [
    path('me/', ProfileMeView.as_view(), name='profile-me'),
]
