"""
URL-конфигурация для эндпоинтов аутентификации и профиля пользователя.
"""
from django.urls import path

from apps.users.views import (
    ClientRegistrationView,
    EmailConfirmView,
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
    TokenRefreshView,
)

app_name = 'users'

urlpatterns = [
    # Регистрация
    path(
        'register/client/',
        ClientRegistrationView.as_view(),
        name='register-client',
    ),

    # Аутентификация
    path(
        'login/',
        LoginView.as_view(),
        name='login',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token-refresh',
    ),

    # Подтверждение email
    path(
        'confirm-email/<uuid:token>/',
        EmailConfirmView.as_view(),
        name='confirm-email',
    ),

    # Сброс пароля
    path(
        'password-reset/',
        PasswordResetView.as_view(),
        name='password-reset',
    ),
    path(
        'password-reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm',
    ),
]
