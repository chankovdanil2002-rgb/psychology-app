"""
Модель отзыва клиента о завершённом приёме.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """
    Отзыв клиента о завершённом приёме.

    Один отзыв на один приём (OneToOne). Рейтинг — целое число 1–5.
    """

    appointment = models.OneToOneField(
        'appointments.Appointment',
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='appointment',
    )
    rating = models.IntegerField(
        'rating',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Оценка от 1 (хуже всего) до 5 (отлично).',
    )
    text = models.TextField(
        'review text',
    )
    created_at = models.DateTimeField(
        'created at',
        auto_now_add=True,
    )

    class Meta:
        db_table = 'reviews'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f'Review for appointment #{self.appointment_id} ({self.rating}/5)'
