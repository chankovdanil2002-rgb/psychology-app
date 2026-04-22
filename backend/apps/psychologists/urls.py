"""
URL-конфигурация приложения psychologists.
"""
from django.urls import path

from apps.psychologists.views import (
    AdminPsychologistListCreateView,
    PsychologistDetailView,
    PsychologistListView,
)

app_name = 'psychologists'

urlpatterns = [
    # Публичный каталог
    path('', PsychologistListView.as_view(), name='psychologist-list'),
    path('<int:pk>/', PsychologistDetailView.as_view(), name='psychologist-detail'),
]

# Административные эндпоинты управления психологами (подключаются отдельно)
admin_urlpatterns = [
    path(
        'psychologists/',
        AdminPsychologistListCreateView.as_view(),
        name='admin-psychologists',
    ),
]
