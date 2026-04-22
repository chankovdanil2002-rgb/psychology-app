"""
Представления для аутентификации, регистрации, подтверждения email и доступа к профилю.
"""
import logging

from django.core.cache import cache
from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from apps.users.models import EmailConfirmationToken, User
from apps.users.serializers import (
    ClientRegistrationSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    UserSerializer,
)
from apps.users.tasks import send_confirmation_email, send_password_reset_email
from apps.users.utils import success_response

logger = logging.getLogger(__name__)


class ClientRegistrationView(GenericAPIView):
    """
    POST /api/auth/register/client/

    Регистрирует нового клиента. Создаёт User (is_active=False) и
    отправляет письмо с подтверждением через Celery.
    """

    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Создаём токен подтверждения email.
        token = EmailConfirmationToken.objects.create(user=user)

        # Асинхронно отправляем письмо с подтверждением.
        send_confirmation_email(user.email, str(token.token))

        return success_response(
            data=UserSerializer(user).data,
            message='Registration successful. Please check your email to confirm your account.',
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    """
    POST /api/auth/login/

    Аутентифицирует пользователя и возвращает JWT access- и refresh-токены.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return success_response(
            data={
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
            },
            message='Login successful.',
        )


class EmailConfirmView(GenericAPIView):
    """
    GET /api/auth/confirm-email/<token>/

    Активирует аккаунт пользователя, проверяя токен подтверждения.
    """

    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            confirmation = EmailConfirmationToken.objects.select_related(
                'user'
            ).get(token=token)
        except EmailConfirmationToken.DoesNotExist:
            return success_response(
                message='Invalid confirmation token.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if confirmation.is_used:
            return success_response(
                message='This token has already been used.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if confirmation.is_expired:
            return success_response(
                message='This token has expired.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Активируем пользователя.
        user = confirmation.user
        user.is_active = True
        user.save(update_fields=['is_active'])

        # Помечаем токен как использованный.
        confirmation.is_used = True
        confirmation.save(update_fields=['is_used'])

        return success_response(
            message='Email confirmed successfully. You can now log in.',
        )


class PasswordResetView(GenericAPIView):
    """
    POST /api/auth/password-reset/

    Инициирует сброс пароля. Если пользователь существует, отправляет письмо.
    Всегда возвращает success, чтобы не раскрывать наличие email в системе.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, is_active=True)
            token = EmailConfirmationToken.objects.create(user=user)
            send_password_reset_email(user.email, str(token.token))
        except User.DoesNotExist:
            pass  # Не раскрываем, существует ли такой email.

        return success_response(
            message='If your email is registered, you will receive a password reset link.',
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    POST /api/auth/password-reset/confirm/

    Устанавливает новый пароль по валидному токену сброса.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_uuid = serializer.validated_data['token']
        new_password = serializer.validated_data['password']

        try:
            confirmation = EmailConfirmationToken.objects.select_related(
                'user'
            ).get(token=token_uuid)
        except EmailConfirmationToken.DoesNotExist:
            return success_response(
                message='Invalid reset token.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not confirmation.is_valid:
            return success_response(
                message='This token has expired or already been used.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Обновляем пароль.
        user = confirmation.user
        user.set_password(new_password)
        user.save(update_fields=['password'])

        # Помечаем токен как использованный.
        confirmation.is_used = True
        confirmation.save(update_fields=['is_used'])

        return success_response(
            message='Password has been reset successfully.',
        )


class TokenRefreshView(BaseTokenRefreshView):
    """
    POST /api/auth/token/refresh/

    Обновляет JWT access-токен по валидному refresh-токену.
    Наследуется от встроенного TokenRefreshView из SimpleJWT.
    """

    pass


class ProfileMeView(GenericAPIView):
    """
    GET/PUT/PATCH /api/profile/me/

    Возвращает или обновляет профиль текущего пользователя.
    Определяет роль и делегирует работу подходящему сериализатору.
    """

    permission_classes = [IsAuthenticated]

    def get_profile_and_serializer(self, user):
        """
        Возвращает (profile_instance, serializer_class) в зависимости от роли пользователя.

        Использует ленивые импорты, чтобы избежать циклических зависимостей.
        """
        if user.role == User.Role.CLIENT:
            from apps.clients.models import ClientProfile
            from apps.clients.serializers import ClientProfileSerializer

            profile, _ = ClientProfile.objects.get_or_create(user=user)
            return profile, ClientProfileSerializer

        if user.role == User.Role.PSYCHOLOGIST:
            from apps.psychologists.models import PsychologistProfile
            from apps.psychologists.serializers import PsychologistProfileSerializer

            profile, _ = PsychologistProfile.objects.get_or_create(user=user)
            return profile, PsychologistProfileSerializer

        # Админ или неизвестная роль — возвращаем базовую информацию о пользователе.
        return None, UserSerializer

    def get(self, request):
        """Возвращает данные профиля текущего пользователя (кэшируется по пользователю)."""
        cache_key = f'profile_{request.user.id}'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return success_response(data=cached_data, message='Profile retrieved.')

        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            # Админ — возвращаем базовые данные пользователя.
            data = serializer_class(request.user).data
        else:
            data = serializer_class(profile).data

        cache.set(cache_key, data, 300)  # Кэшируем на 5 минут.
        return success_response(data=data, message='Profile retrieved.')

    def put(self, request):
        """Полное обновление профиля текущего пользователя."""
        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            return success_response(
                message='Admin profiles cannot be updated via this endpoint.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(
            profile, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Инвалидируем кэш профиля пользователя после обновления.
        cache.delete(f'profile_{request.user.id}')

        return success_response(
            data=serializer.data,
            message='Profile updated.',
        )

    def patch(self, request):
        """Частичное обновление профиля текущего пользователя."""
        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            return success_response(
                message='Admin profiles cannot be updated via this endpoint.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(
            profile,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Инвалидируем кэш профиля пользователя после обновления.
        cache.delete(f'profile_{request.user.id}')

        return success_response(
            data=serializer.data,
            message='Profile updated.',
        )
