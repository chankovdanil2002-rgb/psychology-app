"""
Кастомная модель пользователя и токен подтверждения email для приложения записи к психологу.

Использует email как основной идентификатор вместо username.
"""
import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Кастомный менеджер модели User, использующий email как уникальный идентификатор."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает обычного пользователя с указанным email и паролем.

        Args:
            email: Email пользователя (обязательный, используется как логин).
            password: Пароль пользователя.
            **extra_fields: Дополнительные поля модели User.

        Returns:
            Вновь созданный экземпляр User.

        Raises:
            ValueError: Если email не указан.
        """
        if not email:
            raise ValueError('The Email field must be set.')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает суперпользователя с указанным email и паролем.

        Суперпользователи автоматически активны, являются staff и имеют роль администратора.

        Args:
            email: Email суперпользователя.
            password: Пароль суперпользователя.
            **extra_fields: Дополнительные поля модели User.

        Returns:
            Вновь созданный экземпляр суперпользователя.

        Raises:
            ValueError: Если is_staff или is_superuser не True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя, использующая email как уникальный идентификатор.

    Поля:
        email: Уникальный email, используемый для аутентификации.
        role: Роль пользователя (клиент, психолог или админ).
        is_active: Подтвердил ли пользователь свой email.
        is_staff: Имеет ли пользователь доступ к Django admin.
        date_joined: Время создания аккаунта.
    """

    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        PSYCHOLOGIST = 'psychologist', 'Psychologist'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(
        'email address',
        unique=True,
        db_index=True,
    )
    role = models.CharField(
        'role',
        max_length=15,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text='Designates whether the user has confirmed their email.',
    )
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can access the admin site.',
    )
    date_joined = models.DateTimeField(
        'date joined',
        default=timezone.now,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def is_client(self):
        """Проверяет, что пользователь имеет роль клиента."""
        return self.role == self.Role.CLIENT

    @property
    def is_psychologist(self):
        """Проверяет, что пользователь имеет роль психолога."""
        return self.role == self.Role.PSYCHOLOGIST

    @property
    def is_admin(self):
        """Проверяет, что пользователь имеет роль администратора."""
        return self.role == self.Role.ADMIN


class EmailConfirmationToken(models.Model):
    """
    Токен подтверждения email-адреса.

    Генерируется при регистрации пользователя и отправляется по email.
    По умолчанию истекает через 24 часа (настраивается в settings).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='email_confirmation_tokens',
        verbose_name='user',
    )
    token = models.UUIDField(
        'token',
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    code = models.CharField(
        'code',
        max_length=6,
        blank=True,
        db_index=True,
    )
    is_used = models.BooleanField(
        'used',
        default=False,
    )
    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
    )
    expires_at = models.DateTimeField(
        'expires at',
    )

    class Meta:
        db_table = 'email_confirmation_tokens'
        verbose_name = 'email confirmation token'
        verbose_name_plural = 'email confirmation tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f'Token for {self.user.email} (used={self.is_used})'

    def save(self, *args, **kwargs):
        """Устанавливает время истечения при первом сохранении, если оно ещё не задано."""
        if not self.code:
            self.code = f'{secrets.randbelow(1_000_000):06d}'
        if not self.expires_at:
            expiry_hours = getattr(
                settings,
                'EMAIL_CONFIRMATION_TOKEN_EXPIRY_HOURS',
                24,
            )
            self.expires_at = timezone.now() + timedelta(
                hours=expiry_hours
            )
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Проверяет, истёк ли срок действия токена."""
        return timezone.now() > self.expires_at

    @property
    def is_valid(self):
        """Проверяет, пригоден ли токен (не использован и не истёк)."""
        return not self.is_used and not self.is_expired
