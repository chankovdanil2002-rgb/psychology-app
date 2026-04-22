"""
Вспомогательные функции для отправки email.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_confirmation_email(user_email, token):
    """Отправляет ссылку подтверждения email новому зарегистрированному пользователю."""
    confirmation_url = f'{settings.FRONTEND_URL}/confirm-email/{token}'

    subject = 'Подтверждение регистрации — Psychology App'
    message = (
        f'Здравствуйте!\n\n'
        f'Для подтверждения вашей регистрации перейдите по ссылке:\n'
        f'{confirmation_url}\n\n'
        f'Ссылка действительна в течение 24 часов.\n\n'
        f'Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.\n\n'
        f'С уважением,\nКоманда Psychology App'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info('Confirmation email sent to %s', user_email)
    except Exception as exc:
        logger.error('Failed to send confirmation email to %s: %s', user_email, exc)


def send_password_reset_email(user_email, token):
    """Отправляет пользователю ссылку для сброса пароля."""
    reset_url = f'{settings.FRONTEND_URL}/reset-password/{token}'

    subject = 'Сброс пароля — Psychology App'
    message = (
        f'Здравствуйте!\n\n'
        f'Для сброса пароля перейдите по ссылке:\n'
        f'{reset_url}\n\n'
        f'Ссылка действительна в течение 24 часов.\n\n'
        f'Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.\n\n'
        f'С уважением,\nКоманда Psychology App'
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info('Password reset email sent to %s', user_email)
    except Exception as exc:
        logger.error('Failed to send password reset email to %s: %s', user_email, exc)
