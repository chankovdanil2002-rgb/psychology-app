"""
Модель внутрисистемного уведомления пользователю.
"""
from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Внутрисистемное уведомление для пользователя."""

    class NotificationType(models.TextChoices):
        APPOINTMENT_CONFIRMED = "appointment_confirmed", "Appointment Confirmed"
        APPOINTMENT_REJECTED = "appointment_rejected", "Appointment Rejected"
        APPOINTMENT_CANCELLED = "appointment_cancelled", "Appointment Cancelled"
        APPOINTMENT_COMPLETED = "appointment_completed", "Appointment Completed"
        REVIEW_REQUEST = "review_request", "Review Request"
        VERIFICATION_APPROVED = "verification_approved", "Verification Approved"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM,
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.user.email}"
