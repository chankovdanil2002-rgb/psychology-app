"""
Модели специализаций и связующей таблицы «психолог — специализация».
"""
from django.db import models


class Specialization(models.Model):
    """
    Психологическая специализация (например, КПТ, семейная терапия).

    Используется для категоризации психологов и фильтрации каталога.
    """

    name = models.CharField(
        'name',
        max_length=200,
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        max_length=200,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        'description',
        blank=True,
        default='',
    )
    icon = models.CharField(
        'icon',
        max_length=100,
        blank=True,
        null=True,
        help_text='Необязательный идентификатор иконки или CSS-класс.',
    )

    class Meta:
        db_table = 'specializations'
        verbose_name = 'specialization'
        verbose_name_plural = 'specializations'
        ordering = ['name']

    def __str__(self):
        return self.name


class PsychologistSpecialization(models.Model):
    """
    Связующая таблица M2M: психолог — специализация.

    Позволяет отметить одну специализацию как основную (profile-defining) для психолога.
    """

    psychologist = models.ForeignKey(
        'psychologists.PsychologistProfile',
        on_delete=models.CASCADE,
        related_name='psychologist_specializations',
        verbose_name='psychologist',
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name='psychologist_specializations',
        verbose_name='specialization',
    )
    is_primary = models.BooleanField(
        'primary specialization',
        default=False,
    )

    class Meta:
        db_table = 'psychologist_specializations'
        verbose_name = 'psychologist specialization'
        verbose_name_plural = 'psychologist specializations'
        unique_together = ('psychologist', 'specialization')

    def __str__(self):
        primary_label = ' (основная)' if self.is_primary else ''
        return f'{self.psychologist} — {self.specialization}{primary_label}'
