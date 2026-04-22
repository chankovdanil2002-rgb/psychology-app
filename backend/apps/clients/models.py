"""
Модель профиля клиента.

Каждый пользователь с ролью 'client' имеет связанный один-к-одному ClientProfile,
где хранится персональная информация и флаг заполненности профиля.
"""
from django.conf import settings
from django.db import models


class ClientProfile(models.Model):
    """
    Расширенный профиль пользователя-клиента.

    Создаётся автоматически через post_save-сигнал модели User
    (см. apps.users.signals). Клиенты должны заполнить обязательные поля
    и установить is_profile_complete=True, прежде чем смогут записываться на приём.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile',
        verbose_name='user',
    )
    first_name = models.CharField(
        'first name',
        max_length=100,
        blank=True,
        default='',
    )
    last_name = models.CharField(
        'last name',
        max_length=100,
        blank=True,
        default='',
    )
    phone = models.CharField(
        'phone number',
        max_length=20,
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        'date of birth',
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        'avatar',
        upload_to='clients/avatars/',
        blank=True,
        null=True,
    )
    is_profile_complete = models.BooleanField(
        'profile complete',
        default=False,
        help_text='Set to True once the client has filled in all required fields.',
    )

    class Meta:
        db_table = 'client_profiles'
        verbose_name = 'client profile'
        verbose_name_plural = 'client profiles'

    def __str__(self):
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.user.email

    def save(self, *args, **kwargs):
        """Автоматически ставит is_profile_complete, когда все обязательные поля заполнены."""
        self.is_profile_complete = all([
            self.first_name,
            self.last_name,
            self.phone,
            self.date_of_birth,
        ])
        super().save(*args, **kwargs)
