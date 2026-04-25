"""
Сериализаторы для аутентификации, регистрации и управления профилем пользователя.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import User


class ClientRegistrationSerializer(serializers.Serializer):
    """
    Сериализатор регистрации клиента.

    Проверяет уникальность email, надёжность пароля и совпадение подтверждения.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    def validate_email(self, value):
        """Проверяет, что email ещё не зарегистрирован."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return email

    def validate_password(self, value):
        """Запускает встроенные валидаторы паролей Django."""
        validate_password(value)
        return value

    def validate(self, attrs):
        """Проверяет совпадение двух введённых паролей."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return attrs

    def create(self, validated_data):
        """Создаёт нового пользователя-клиента (неактивного до подтверждения email)."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.CLIENT,
        )
        return user


class PsychologistRegistrationSerializer(serializers.Serializer):
    """
    Сериализатор регистрации психолога.

    Включает персональные данные и загрузку скана диплома.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    patronymic = serializers.CharField(max_length=150, required=False, allow_blank=True)
    diploma_scan = serializers.FileField()

    def validate_email(self, value):
        """Проверяет, что email ещё не зарегистрирован."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.'
            )
        return email

    def validate_password(self, value):
        """Запускает встроенные валидаторы паролей Django."""
        validate_password(value)
        return value

    def validate_diploma_scan(self, value):
        """Проверяет тип и размер файла со сканом диплома."""
        max_size = 5 * 1024 * 1024  # 5 МБ
        allowed_types = [
            'image/jpeg',
            'image/png',
            'image/webp',
            'application/pdf',
        ]

        if value.size > max_size:
            raise serializers.ValidationError(
                'File size must not exceed 5 MB.'
            )
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                'Allowed file types: JPEG, PNG, WebP, PDF.'
            )
        return value

    def validate(self, attrs):
        """Проверяет совпадение двух введённых паролей."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return attrs

    def create(self, validated_data):
        """
        Создаёт нового пользователя-психолога и его профиль.

        PsychologistProfile создаётся во view после сохранения пользователя,
        поскольку модель профиля живёт в приложении psychologists.
        """
        validated_data.pop('password_confirm')
        diploma_scan = validated_data.pop('diploma_scan')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        patronymic = validated_data.pop('patronymic', '')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.PSYCHOLOGIST,
        )

        # Сохраняем дополнительные поля в экземпляре сериализатора для дальнейшего использования во view.
        self._psychologist_extra = {
            'first_name': first_name,
            'last_name': last_name,
            'patronymic': patronymic,
            'diploma_scan': diploma_scan,
        }

        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор входа пользователя.

    Проверяет учётные данные и возвращает аутентифицированного пользователя.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, attrs):
        """Аутентифицирует пользователя по переданным учётным данным."""
        email = attrs.get('email', '').lower()
        password = attrs.get('password', '')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                'Invalid email or password.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Please confirm your email address before logging in.'
            )

        attrs['user'] = user
        return attrs


class EmailCodeConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.RegexField(
        regex=r'^\d{6}$',
        max_length=6,
        min_length=6,
        error_messages={
            'invalid': 'Введите 6 цифр из письма.',
        },
    )

    def validate_email(self, value):
        return value.lower()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор только для чтения базовой информации о пользователе."""

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = fields


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор для инициации сброса пароля (отправляет email с токеном)."""

    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Нормализует email. Мы не раскрываем, существует ли этот email:
        view всегда возвращает сообщение об успехе.
        """
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор установки нового пароля по токену сброса."""

    token = serializers.UUIDField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    def validate_password(self, value):
        """Запускает встроенные валидаторы паролей Django."""
        validate_password(value)
        return value

    def validate(self, attrs):
        """Проверяет совпадение двух введённых паролей."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор JWT-токена, добавляющий роль пользователя в claims токена.
    """

    @classmethod
    def get_token(cls, user):
        """Добавляет кастомные claims (role) в JWT-токен."""
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token
