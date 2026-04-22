"""
Модель тайм-слота для управления расписанием психолога.
"""
from django.db import models


class TimeSlot(models.Model):
    """
    Один доступный для бронирования тайм-слот в расписании психолога.

    Каждый слот представляет конкретную дату и временной диапазон, в течение
    которого психолог доступен для приёма.
    """

    psychologist = models.ForeignKey(
        'psychologists.PsychologistProfile',
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name='psychologist',
    )
    date = models.DateField(
        'date',
        db_index=True,
    )
    start_time = models.TimeField(
        'start time',
    )
    end_time = models.TimeField(
        'end time',
    )
    is_available = models.BooleanField(
        'available',
        default=True,
        help_text='False, если этот слот уже забронирован клиентом.',
    )

    class Meta:
        db_table = 'time_slots'
        verbose_name = 'time slot'
        verbose_name_plural = 'time slots'
        unique_together = ('psychologist', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return (
            f'{self.psychologist} | {self.date} '
            f'{self.start_time:%H:%M}–{self.end_time:%H:%M}'
        )
