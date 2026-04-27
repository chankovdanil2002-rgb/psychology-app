"""
Представления для аутентификации, регистрации, подтверждения email и доступа к профилю.
"""
import logging
import secrets
from datetime import timedelta

from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from apps.users.models import EmailConfirmationToken, User
from apps.users.serializers import (
    ClientRegistrationSerializer,
    EmailCodeConfirmationSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    UserSerializer,
)
from apps.users.tasks import (
    EmailDeliveryError,
    send_confirmation_email,
    send_password_reset_email,
)
from apps.users.utils import success_response

logger = logging.getLogger(__name__)


class EmailDeliveryAPIException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Не удалось отправить письмо. Проверьте настройки почты.'
    default_code = 'email_delivery_failed'


class ClientRegistrationView(GenericAPIView):
    """
    POST /api/auth/register/client/

    Регистрирует нового клиента. Данные временно сохраняются в кэше (24 ч),
    пользователь в БД не создаётся до подтверждения кода из письма.
    """

    serializer_class = ClientRegistrationSerializer
    permission_classes = [AllowAny]

    # Время жизни ожидающей регистрации — 24 часа.
    _PENDING_TTL = 60 * 60 * 24

    @staticmethod
    def _cache_key(email: str) -> str:
        return f'pending_reg:{email}'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Генерируем 6-значный код подтверждения.
        code = f'{secrets.randbelow(1_000_000):06d}'
        expires_at = timezone.now() + timedelta(hours=24)

        # Сохраняем данные регистрации в кэше — БД ещё не трогаем.
        cache.set(
            self._cache_key(email),
            {
                'email': email,
                'password': password,
                'role': User.Role.CLIENT,
                'code': code,
                'expires_at': expires_at,
            },
            self._PENDING_TTL,
        )

        try:
            send_confirmation_email(email, code)
        except EmailDeliveryError as exc:
            cache.delete(self._cache_key(email))
            raise EmailDeliveryAPIException(str(exc)) from exc

        return success_response(
            data={'email': email},
            message='Регистрация прошла успешно. Проверьте почту и введите код подтверждения.',
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
            message='Вход выполнен успешно.',
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
                message='Недействительная ссылка подтверждения.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if confirmation.is_used:
            return success_response(
                message='Эта ссылка уже была использована.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if confirmation.is_expired:
            return success_response(
                message='Срок действия ссылки истёк.',
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
            message='Email подтверждён. Теперь вы можете войти в систему.',
        )


class EmailCodeConfirmView(GenericAPIView):
    """
    POST /api/auth/confirm-email/code/

    Подтверждает email и создаёт пользователя в БД.
    Данные регистрации берутся из кэша по email + код.
    """

    serializer_class = EmailCodeConfirmationSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def _cache_key(email: str) -> str:
        return f'pending_reg:{email}'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        pending = cache.get(self._cache_key(email))

        if pending is None or pending.get('code') != code:
            return success_response(
                message='Неверный код подтверждения.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if timezone.now() > pending['expires_at']:
            cache.delete(self._cache_key(email))
            return success_response(
                message='Срок действия кода истёк. Зарегистрируйтесь снова.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Защита от гонки: если пользователь уже создан (повторный запрос).
        if User.objects.filter(email=email).exists():
            cache.delete(self._cache_key(email))
            return success_response(
                message='Аккаунт уже подтверждён. Войдите в систему.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Создаём пользователя — уже активным, email подтверждён.
        with transaction.atomic():
            user = User.objects.create_user(
                email=pending['email'],
                password=pending['password'],
                role=pending['role'],
                is_active=True,
            )

        # Удаляем данные ожидания из кэша.
        cache.delete(self._cache_key(email))

        return success_response(
            data=UserSerializer(user).data,
            message='Email подтверждён. Теперь можно войти.',
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
            try:
                send_password_reset_email(user.email, str(token.token))
            except EmailDeliveryError as exc:
                raise EmailDeliveryAPIException(str(exc)) from exc
        except User.DoesNotExist:
            pass  # Не раскрываем, существует ли такой email.

        return success_response(
            message='Если этот email зарегистрирован, вы получите письмо со ссылкой для сброса пароля.',
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
                message='Недействительная ссылка сброса пароля.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if not confirmation.is_valid:
            return success_response(
                message='Срок действия ссылки истёк или она уже была использована.',
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
            message='Пароль успешно изменён.',
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
            return success_response(data=cached_data, message='Профиль получен.')

        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            # Админ — возвращаем базовые данные пользователя.
            data = serializer_class(request.user).data
        else:
            data = serializer_class(profile).data

        cache.set(cache_key, data, 300)  # Кэшируем на 5 минут.
        return success_response(data=data, message='Профиль получен.')

    def put(self, request):
        """Полное обновление профиля текущего пользователя."""
        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            return success_response(
                message='Профиль администратора нельзя обновить через этот эндпоинт.',
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
            message='Профиль обновлён.',
        )

    def patch(self, request):
        """Частичное обновление профиля текущего пользователя."""
        profile, serializer_class = self.get_profile_and_serializer(
            request.user
        )

        if profile is None:
            return success_response(
                message='Профиль администратора нельзя обновить через этот эндпоинт.',
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
            message='Профиль обновлён.',
        )
