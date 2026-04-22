"""
Сигналы для автоматического создания профиля при регистрации пользователя.

Использует ленивые импорты, чтобы избежать циклических зависимостей
с приложениями clients и psychologists.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создаёт соответствующий профиль при создании нового User.

    - role='client'       -> ClientProfile
    - role='psychologist' -> PsychologistProfile
    - role='admin'        -> профиль не требуется
    """
    if not created:
        return

    if instance.role == User.Role.CLIENT:
        # Ленивый импорт для избежания циклических зависимостей.
        from apps.clients.models import ClientProfile

        ClientProfile.objects.get_or_create(user=instance)
        logger.info(
            'ClientProfile created for user %s', instance.email
        )

    elif instance.role == User.Role.PSYCHOLOGIST:
        # Ленивый импорт для избежания циклических зависимостей.
        from apps.psychologists.models import PsychologistProfile

        PsychologistProfile.objects.get_or_create(user=instance)
        logger.info(
            'PsychologistProfile created for user %s', instance.email
        )
