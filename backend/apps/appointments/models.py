"""
Модель записи на приём к психологу.
"""
from django.db import models
from django.db.models import Q


class Appointment(models.Model):
    """
    Запись на приём, связывающая клиента, психолога и конкретный тайм-слот.

    Жизненный цикл статусов:
        pending → confirmed → completed
        pending → rejected
        pending → cancelled (отменена клиентом)
        confirmed → cancelled (отменена клиентом)
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'

    client = models.ForeignKey(
        'clients.ClientProfile',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='client',
    )
    psychologist = models.ForeignKey(
        'psychologists.PsychologistProfile',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='psychologist',
    )
    time_slot = models.ForeignKey(
        'schedule.TimeSlot',
        on_delete=models.PROTECT,
        related_name='appointments',
        verbose_name='time slot',
    )
    status = models.CharField(
        'status',
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    comment = models.TextField(
        'client comment',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'updated at',
        auto_now=True,
    )

    class Meta:
        db_table = 'appointments'
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['time_slot'],
                condition=Q(status__in=['pending', 'confirmed']),
                name='unique_active_appointment_per_time_slot',
            ),
        ]

    def __str__(self):
        return (
            f'Appointment #{self.pk}: {self.client} -> {self.psychologist} '
            f'({self.status})'
        )
