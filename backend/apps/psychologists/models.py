"""
Модель профиля психолога.

Каждый пользователь с ролью 'psychologist' имеет связанный один-к-одному PsychologistProfile
с профессиональной информацией, статусом верификации и ценой.
"""
from django.conf import settings
from django.db import models


class PsychologistProfile(models.Model):
    """
    Расширенный профиль пользователя-психолога.

    Создаётся автоматически через post_save-сигнал модели User
    (см. apps.users.signals). После регистрации психолог должен быть
    верифицирован администратором, прежде чем его профиль станет виден в каталоге.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='psychologist_profile',
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
    patronymic = models.CharField(
        'patronymic',
        max_length=100,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        'phone number',
        max_length=20,
        blank=True,
        null=True,
    )
    photo = models.TextField(
        'profile photo image',
        blank=True,
        default='',
        help_text='Base64 data URL with the psychologist profile photo.',
    )
    experience_years = models.IntegerField(
        'years of experience',
        blank=True,
        null=True,
    )
    education = models.TextField(
        'education',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        'biography',
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        'session price',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    diploma_scan = models.FileField(
        'diploma scan',
        upload_to='psychologists/diplomas/',
        blank=True,
    )
    specializations = models.ManyToManyField(
        'specializations.Specialization',
        through='specializations.PsychologistSpecialization',
        related_name='psychologists',
        blank=True,
    )
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to True once an admin has verified the diploma.',
    )
    verified_at = models.DateTimeField(
        'verified at',
        blank=True,
        null=True,
    )
    is_profile_complete = models.BooleanField(
        'profile complete',
        default=False,
        help_text='Set to True once the psychologist has filled in all required fields.',
    )

    class Meta:
        db_table = 'psychologist_profiles'
        verbose_name = 'psychologist profile'
        verbose_name_plural = 'psychologist profiles'

    def save(self, *args, **kwargs):
        """Автоматически ставит is_profile_complete, когда заполнены все обязательные поля."""
        self.is_profile_complete = all([
            self.first_name,
            self.last_name,
            self.phone,
            self.experience_years is not None,
            self.education,
            self.bio,
            self.price is not None,
        ])
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        full_name = ' '.join(p for p in parts if p)
        return full_name if full_name else self.user.email

    def get_average_rating(self):
        """
        Вычисляет средний рейтинг по отзывам на все завершённые приёмы.

        Замечание: для списочных view предпочтительнее использовать аннотации queryset (Avg),
        чтобы избежать N+1. Этот метод — для работы с одиночным экземпляром.

        Returns:
            float или None: Средний рейтинг (1-5) или None, если отзывов нет.
        """
        from django.db.models import Avg

        result = (
            self.appointments
            .filter(status='completed', review__isnull=False)
            .aggregate(avg=Avg('review__rating'))
        )
        avg = result['avg']
        return round(avg, 2) if avg is not None else None

    def get_total_reviews(self):
        """
        Считает общее количество отзывов у этого психолога.

        Замечание: для списочных view предпочтительнее использовать аннотации (Count).

        Returns:
            int: Количество отзывов.
        """
        return (
            self.appointments
            .filter(status='completed', review__isnull=False)
            .count()
        )
