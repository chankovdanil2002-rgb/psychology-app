import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EmailDeliveryError(Exception):
    pass


def build_password_reset_url(token):
    return f'{settings.FRONTEND_URL.rstrip("/")}/reset-password/{token}'


def send_confirmation_email(user_email, code):
    subject = 'Код подтверждения регистрации - Psychology App'
    message = (
        f'Здравствуйте!\n\n'
        f'Ваш код подтверждения регистрации: {code}\n\n'
        f'Введите этот код на сайте, чтобы активировать аккаунт.\n'
        f'Код действителен в течение 24 часов.\n\n'
        f'Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.\n\n'
        f'С уважением,\nКоманда Psychology App'
    )

    _send_email(subject, message, user_email, 'письмо подтверждения')


def send_password_reset_email(user_email, token):
    reset_url = build_password_reset_url(token)

    subject = 'Сброс пароля - Psychology App'
    message = (
        f'Здравствуйте!\n\n'
        f'Для сброса пароля перейдите по ссылке:\n'
        f'{reset_url}\n\n'
        f'Ссылка действительна в течение 24 часов.\n\n'
        f'Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.\n\n'
        f'С уважением,\nКоманда Psychology App'
    )

    _send_email(subject, message, user_email, 'письмо для сброса пароля')


def _send_email(subject, message, recipient, description):
    try:
        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info('%s sent to %s', description, recipient)
    except Exception as exc:
        logger.exception('Failed to send %s to %s', description, recipient)
        raise EmailDeliveryError(
            f'Не удалось отправить {description}. Проверьте настройки почты.'
        ) from exc

    if sent_count == 0:
        raise EmailDeliveryError(
            f'Почтовый сервер не принял {description}.'
        )
